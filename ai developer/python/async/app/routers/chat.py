from fastapi import APIRouter, Depends, HTTPException, status
import asyncio
from ..services.ai import call_llm
from ..auth import get_current_user
from ..services.ministralai import get_assistant_reply,generate_flashcards_async, generate_quiz_async, generate_summary_async
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
    
    
@router.post("/study-pack", response_model=StudyPackResponse)
async def generate_study_pack(
    payload: StudyPackRequest,
    # background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """
    Generates summary, quiz, and flashcards CONCURRENTLY using asyncio.gather.
    """
    try:
        # Run three independent async AI tasks concurrently with timeout
        summary_res, quiz_res, flashcard_res = await asyncio.wait_for(
            asyncio.gather(
                generate_summary_async(payload.topic),
                generate_quiz_async(payload.topic),
                generate_flashcards_async(payload.topic)
            ),
            timeout=8.0
        )

        # Trigger non-blocking background task
        # background_tasks.add_task(log_analytics_background, current_user.id, "generate_study_pack")

        return StudyPackResponse(
            summary=summary_res,
            quiz=quiz_res,
            flashcards=flashcard_res
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Generating the full study pack timed out."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating study pack: {str(e)}"
        )