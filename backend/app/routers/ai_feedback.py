from fastapi import APIRouter

router = APIRouter(prefix="/ai-feedback", tags=["AI Feedback"])

@router.get("/")
def get_ai_feedback_status():
    return {"message": "AI Feedback router is working"}
