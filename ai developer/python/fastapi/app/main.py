from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone

from pydantic import BaseModel, Field
from app.routers import chat

app = FastAPI(

title="My Backend API",

description="A first FastAPI backend for my project.",

version="1.0.0"

)

app.include_router(chat.router)

@app.get("/")
def health():

    return{
        "status": "ok",

        "message": "API is running",

        "timestamp": datetime.now(timezone.utc).isoformat(),

        "version": "1.0.0"
    }


@app.get("/about")
def about():

    return {

    "project": "My FastAPI backend",

    "purpose": "Expose Python features through an API",

    "status": "learning backend fundamentals"

    }


class QuizRequest(BaseModel):

    topic: str = Field(..., min_length=2, max_length=100)

    num_questions: int = Field(default=3, ge=1, le=10)

@app.post("/quiz")

def quiz(request: QuizRequest):

    questions = []

    for index in range(1, request.num_questions + 1):

        questions.append({

            "question": f"Question {index} about {request.topic}",

            "options": ["Option A", "Option B", "Option C", "Option D"],

            "answer": "Option A"

        })

    return {

        "topic": request.topic,

        "num_questions": request.num_questions,

        "questions": questions

    }



class SummariseRequest(BaseModel):

    text: str = Field(..., min_length=20, max_length=5000)

    max_bullets: int = Field(default=3, ge=1, le=5)

 

@app.post("/summarise")

def summarise(request: SummariseRequest):

    words = request.text.split()

 

    return {

        "summary": [

            "This is a placeholder summary.",

            "The real summarization logic will be connected later."

        ][:request.max_bullets],

        "word_count": len(words)

    }

class FlashcardRequest(BaseModel):

    topic: str = Field(..., min_length=2, max_length=100)

    count: int = Field(default=3, ge=1, le=10)

class Flashcard(BaseModel):

    front: str

    back: str


class FlashcardResponse(BaseModel):

    topic: str

    flashcards: list[Flashcard]

@app.post("/flashcards", response_model=FlashcardResponse)
def create_flashcards(request: FlashcardRequest):

    clean_topic = request.topic.strip()

    if not clean_topic:

        raise HTTPException(

        status_code=400,

        detail="Topic cannot be empty."

        )

    flashcards = []
    for index in range(1, request.count + 1):

        flashcards.append(

            Flashcard(

            front=f"Flashcard {index}: What is one key idea about {clean_topic}?",

            back=f"This card explains an important idea about {clean_topic}."

            )
        )

        return FlashcardResponse(

            topic=clean_topic,

            flashcards=flashcards

        )