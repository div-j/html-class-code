from fastapi import FastAPI
from langserve import add_routes
from app.agent import get_agent_executor

app = FastAPI(
    title="StudyPulse Agent API",
    version="1.0",
    description="LangServe backend exposing a Llama-3-powered agent"
)

agent_executor = get_agent_executor()

# Expose agent via LangServe under /agent route
add_routes(
    app,
    agent_executor,
    path="/agent"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "LangServe Agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=True)