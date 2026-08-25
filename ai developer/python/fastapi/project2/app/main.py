from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, conversations, chat


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Study Assistant API")

app.include_router(chat.router)

app.include_router(auth.router)
app.include_router(conversations.router)

app.get("/")
def root():
    return {"message": "Study Assistant API is running"}

app.get("/heaalth")
def health():
    return {
        "status":"success",
        "message":"API is healthy",
    }


