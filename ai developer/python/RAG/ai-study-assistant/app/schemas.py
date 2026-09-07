from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    content: str = Field(..., description="User message text")


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class QuizOutput(BaseModel):
    topic: str
    questions: List[QuizQuestion]

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = Field(default=3, ge=1, le=10)