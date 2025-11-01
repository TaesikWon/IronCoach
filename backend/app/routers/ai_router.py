# app/routers/ai_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import analyze_training_session

router = APIRouter(prefix="/ai", tags=["AI Coaching"])

# 요청 데이터 구조
class SessionAnalysisRequest(BaseModel):
    session_id: int
    title: str
    description: str

# API 엔드포인트
@router.post("/analyze")
async def analyze_session(request: SessionAnalysisRequest):
    try:
        analysis = await analyze_training_session(
            request.title, request.description, request.session_id
        )
        return {"feedback": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
