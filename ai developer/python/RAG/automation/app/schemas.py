from pydantic import BaseModel, EmailStr, Field
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
    

# study plan request and response payloads

class StudyPlanRequest(BaseModel):
    event_id: str
    student_email: EmailStr
    topic: str
    lesson_note: str
    difficulty: str

class StudyPlanResponse(BaseModel):
    status: str
    student_email: str
    topic: str
    study_plan: str