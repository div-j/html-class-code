from fastapi import APIRouter, Depends, HTTPException, status
import asyncio
from ..services.ai import call_llm
from ..auth import get_current_user
from ..services.ministralai import get_assistant_reply
from ..schema import ChatResponse, ChatRequest, StudyPackResponse, StudyPackRequest
from ..models.user import User



router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    clean_message = request.message.strip()
    if not clean_message:
        raise HTTPException(

        status_code=400,

        detail="Message cannot be empty."

        )

    result = call_llm(clean_message)

    return ChatResponse(**result)

#study pack response model
async def _generate_summary(topic: str) -> str:
    return await get_assistant_reply(
        f"Write a short, clear summary of: {topic}"
    )

async def _generate_quiz(topic: str) -> str:
    return await get_assistant_reply(
        f"Create 3 short quiz questions about: {topic}"
    )

async def _generate_flashcards(topic: str) -> str:
    return await get_assistant_reply(
        f"Create 4 simple flashcards (question → answer) about: {topic}"
    )
    
@router.post("/chat/study-pack", response_model=StudyPackResponse)
async def create_study_pack(
    body: StudyPackRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generates summary, quiz and flashcards concurrently.
    """
    try:
        summary, quiz, flashcards = await asyncio.wait_for(
            asyncio.gather(
                _generate_summary(body.topic),
                _generate_quiz(body.topic),
                _generate_flashcards(body.topic),
            ),
            timeout=25.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Generating the study pack took too long. Please try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Could not generate the study pack right now.{e}"
        )

    return StudyPackResponse(
        summary=summary,
        quiz=quiz,
        flashcards=flashcards
    )