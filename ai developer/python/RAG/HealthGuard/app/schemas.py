from pydantic import BaseModel, Field
from typing import List, Optional


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
    
    
class MedicalChatRequest(BaseModel):
    message: str
    # history: Optional[List[dict]] = []

class MedicalChatResponse(BaseModel):
    answer: str
    was_blocked: bool = False
    reason: Optional[str] = None