# backend/app/routers/ai_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import analyze_training_session

router = APIRouter(prefix="/ai", tags=["AI Coaching"])

class SessionAnalysisRequest(BaseModel):
    title: str
    description: str

@router.post("/analyze")
async def analyze_session(request: SessionAnalysisRequest):
    try:
        analysis = await analyze_training_session(request.title, request.description)
        return {"feedback": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
