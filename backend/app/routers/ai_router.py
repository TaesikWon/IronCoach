# backend/app/routers/ai_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import analyze_training_session
from app.services.ai_chat_service import chat_with_coach

router = APIRouter(prefix="/ai", tags=["AI Coaching"])

class SessionAnalysisRequest(BaseModel):
    session_id: int
    title: str
    description: str

class ChatRequest(BaseModel):  # 👈 추가
    message: str

@router.post("/analyze")
async def analyze_session(request: SessionAnalysisRequest):
    try:
        analysis = await analyze_training_session(
            request.title, request.description, request.session_id
        )
        return {"feedback": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 💬 대화형 AI 코칭 엔드포인트
@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        reply = await chat_with_coach(request.message)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
