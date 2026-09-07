from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import re

from app.schemas import MedicalChatRequest, MedicalChatResponse
from app.llm import stream_chat_response

router = APIRouter(prefix="/medical", tags=["Medical"])


# ---------- Patterns that are still too dangerous ----------
# We only block clear attempts to prescribe or diagnose
UNSAFE_PATTERNS = [
    r"\b(take|swallow|inject)\s+\d+\s*(mg|ml|tablet|capsule)s?\b",
    r"\b(you have|this is|it is)\s+(malaria|typhoid|HIV|pneumonia|diabetes|hypertension)\b",
    r"\b(stop taking|discontinue)\s+(your\s+)?(medication|drugs|ARVs|insulin)\b",
    r"\bprescri(be|ption)\b",
    r"\b(diagnose|diagnosis)\b",
]

COMPILED_PATTERNS = [re.compile(p, re.IGNORECASE) for p in UNSAFE_PATTERNS]


def contains_unsafe_advice(text: str) -> bool:
    return any(p.search(text) for p in COMPILED_PATTERNS)


# ---------- System prompt – allows basic care, blocks dangerous advice ----------
MEDICAL_SYSTEM_PROMPT = """
You are a careful health-information assistant for people in Nigeria and other parts of Africa.
Many users have limited money or live far from hospitals and pharmacies.

What you CAN do:
- Give general first-aid and basic care advice (rest, fluids, oral rehydration, cooling a fever, hygiene, mosquito protection, etc.)
- Explain common danger signs that mean the person should try to reach help
- Share widely accepted public-health information

What you must NEVER do:
- Diagnose any disease (“you have malaria”, “this is typhoid”)
- Recommend a specific medicine name + dosage
- Tell someone to stop or change their prescribed medication
- Create a full treatment plan

Always speak simply, be practical, and remind the user that you are not a replacement for a health worker.
If symptoms sound serious, clearly say they should try to reach the nearest Primary Health Centre, chemist, or hospital.
"""


@router.post("/chat", response_model=MedicalChatResponse)
async def medical_chat(request: MedicalChatRequest):
    """
    Medical chat that allows basic care advice while blocking
    diagnosis and specific drug recommendations.
    """
    messages = [
        {"role": "system", "content": MEDICAL_SYSTEM_PROMPT},
        {"role": "user", "content": request.message},
    ]

    try:
        # Get the full model response
        chunks = []
        async for chunk in stream_chat_response(messages):
            chunks.append(chunk)
        answer = "".join(chunks).strip()

        # Only intervene if the model crossed the hard safety line
        if contains_unsafe_advice(answer):
            # Instead of a cold refusal, ask the model to rephrase safely
            safety_messages = [
                {"role": "system", "content": MEDICAL_SYSTEM_PROMPT},
                {"role": "user", "content": request.message},
                {"role": "assistant", "content": answer},
                {
                    "role": "user",
                    "content": (
                        "Your previous reply contained specific medical advice that is not allowed. "
                        "Please rewrite it using only general basic-care guidance. "
                        "Do not name any drugs or give dosages. "
                        "Remind the user to seek help if symptoms are serious."
                    ),
                },
            ]

            safe_chunks = []
            async for chunk in stream_chat_response(safety_messages):
                safe_chunks.append(chunk)
            safe_answer = "".join(safe_chunks).strip()

            return MedicalChatResponse(
                answer=safe_answer,
                was_blocked=True,
                reason="Model attempted specific medical advice – response was rewritten"
            )

        return MedicalChatResponse(answer=answer, was_blocked=False)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))