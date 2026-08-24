from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.ai import call_llm


router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str = Field(..., default="", min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    model: str
    tokens_used: int

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