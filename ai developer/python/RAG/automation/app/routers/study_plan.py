from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel, EmailStr
import os
import re
from app.schemas import StudyPlanResponse, StudyPlanRequest

router = APIRouter(tags=["Automation Workflows"])

API_SECRET_TOKEN = os.getenv("WEBHOOK_SECRET_TOKEN", "studypulse_secret_key_123")

# Cache to enforce idempotency in memory (In production, use Redis or DB)
PROCESSED_EVENT_IDS = set()


@router.post("/study-plan", response_model=StudyPlanResponse)
async def generate_study_plan(
    payload: StudyPlanRequest,
    x_webhook_secret: str = Header(None)
):
    # 1. Security Check: Validate Secret Header
    if x_webhook_secret != API_SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Webhook-Secret header."
        )

    # 2. Idempotency Check: Prevent duplicate event processing
    if payload.event_id in PROCESSED_EVENT_IDS:
        return StudyPlanResponse(
            status="skipped_duplicate",
            student_email=payload.student_email,
            topic=payload.topic,
            study_plan="Event already processed."
        )

    # Input Validation
    if not payload.lesson_note.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field 'lesson_note' cannot be empty."
        )

    # 3. AI Processing (Simulated generation)
    generated_plan = (
        f"### Customized Study Plan for {payload.topic} ({payload.difficulty.capitalize()})\n"
        f"1. **Core Review**: Analyze notes regarding {payload.lesson_note[:50]}...\n"
        f"2. **Active Recall**: Complete 3 concept recall questions.\n"
        f"3. **Practice**: Allocate 45 minutes of focused review."
    )

    # Register event as processed
    PROCESSED_EVENT_IDS.add(payload.event_id)

    return StudyPlanResponse(
        status="success",
        student_email=payload.student_email,
        topic=payload.topic,
        study_plan=generated_plan
    )