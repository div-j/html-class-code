from fastapi import FastAPI
from app.routers import ai, study_plan

app = FastAPI(
    title="AI Study Assistant API",
    description="FastAPI service supporting OpenAI and Mistral with streaming and JSON quiz generation."
)

app.include_router(ai.router)
app.include_router(study_plan.router)

@app.get("/")
async def root():
    return {"status": "ok", "message": "AI Study Assistant Service is running."}