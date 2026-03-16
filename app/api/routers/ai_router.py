from fastapi import APIRouter
from pydantic import BaseModel
from app.ai.agent import run_agent


router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    response = run_agent(request.message)

    return {
        "response": response
    }