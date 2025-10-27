from fastapi import APIRouter

router = APIRouter(prefix="/tennis", tags=["Tennis"])

@router.get("/")
def tennis_status():
    return {"message": "Tennis router active 🎾"}
