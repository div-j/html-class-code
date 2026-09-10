from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import ValidationError
import json

from app.schemas import ChatRequest, QuizRequest, QuizOutput
from app.llm import stream_chat_response, generate_json_response

router = APIRouter(tags=["AI"])

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI study assistant. Answer clearly and concisely."
        },
        {
            "role": "user",
            "content": request.content
        }
    ]

    try:
        generator = stream_chat_response(messages)
        return StreamingResponse(generator, media_type="text/plain")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat streaming error: {str(e)}"
        )


@router.post("/quiz", response_model=QuizOutput)
async def quiz_endpoint(request: QuizRequest):
    prompt_messages = [
        {
            "role": "system",
            "content": (
                "You generate structured study quizzes. You MUST return a JSON object with two key fields:\n"
                "- 'topic': string\n"
                "- 'questions': list of objects, each with 'question' (string), "
                "'options' (list of 4 strings), 'correct_answer' (string matching one option), "
                "and 'explanation' (string)."
            )
        },
        {
            "role": "user",
            "content": f"Generate a {request.num_questions}-question quiz on the topic: {request.topic}"
        }
    ]

    try:
        raw_json = await generate_json_response(prompt_messages)
        # Validate JSON output against Pydantic schema
        validated_quiz = QuizOutput.model_validate(raw_json)
        return validated_quiz
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Model generated response that failed schema validation: {e.errors()}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quiz generation error: {str(e)}"
        )