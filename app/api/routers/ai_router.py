from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.agent import run_agent

router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat(request: ChatRequest):

    try:

        response = run_agent(request.message)

        return {
            "response": response
        }

    except Exception as e:

        print("AI ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )