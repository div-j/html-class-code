from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import asyncio
from ..database import get_db
from ..models.user import User
from ..models.message import  Message
from ..models.conversation  import Conversation
from ..schema import ConversationCreate, ConversationOut, MessageResponse, MessageResquest
from ..auth import get_current_user
from ..services.ministralai import get_assistant_reply

router = APIRouter(prefix="/conversations", tags=["conversations"])

def get_owned_conversation(db: Session, conversation_id: int, user: User) -> Conversation:
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    if conv.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to access this conversation")
    return conv


@router.post("/", response_model=ConversationOut, status_code=201)
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conv = Conversation(title=data.title or "New conversation", user_id=current_user.id)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv

@router.post("/{conversation_id}/messages", response_model=list[MessageResquest])
async def add_message(
    conversation_id: int,
    message_in: MessageResquest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    conv = get_owned_conversation(db, conversation_id, current_user)
    
    # Get and Save user message
    user_msg = Message(
        conversation_id=conv.id,
        role="user",
        content=message_in.content
    )
    db.add(user_msg)
    db.flush()
    
    # Build history from existing messages
    history = [
        {"role": m.role, "content": m.content}
        for m in conv.messages
    ]
    
    # Send message to assistant
    try:
        # Timeout after 15 seconds
        assistant_content = await asyncio.wait_for(
            get_assistant_reply(
                user_message=message_in.content,
                history=history
            ),
            timeout=15.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="The AI took too long to respond. Please try again."
        )
    except RuntimeError as e:
        # Temporary API / network failure
        raise HTTPException(
            status_code=502,
            detail="The AI service is temporarily unavailable. Please try again later."
        )
    except Exception:
        # Unexpected error
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the reply."
        )
    # Save assistant message
    assistant_msg = Message(
        conversation_id=conv.id,
        role="assistant",
        content=assistant_content
    )
    db.add(assistant_msg)
    
    db.commit()
    db.refresh(user_msg)
    db.refresh(assistant_msg)

    return [user_msg, assistant_msg]

    
@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])

def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conv = get_owned_conversation(db, conversation_id, current_user)
    return conv.messages


