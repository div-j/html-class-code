from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=128, description="Plain text password")


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="User ID")
    email: EmailStr = Field(..., description="User's email address")


class Token(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class ConversationCreate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200, description="Optional conversation title")


class ConversationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Conversation ID")
    title: Optional[str] = Field(None, description="Conversation title")
    created_at: datetime = Field(..., description="When the conversation was created")


class MessageResquest(BaseModel):
    content: str = Field(..., min_length=1, max_length=4000, description="Message content")


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Message ID")
    role: str = Field(..., description="Role of the message sender (user or assistant)")
    content: str = Field(..., description="Message content")
    tokens_used: int = Field(..., description="Tokens used ")
    created_at: datetime = Field(..., description="When the message was created")
    

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    answer: str
    model: str
    tokens_used: int
    
class StudyPackRequest(BaseModel):
    topic: str

class StudyPackResponse(BaseModel):
    summary: str
    quiz: str
    flashcards: str
    execution_mode: str = "Concurrent (asyncio.gather)"
    
    
