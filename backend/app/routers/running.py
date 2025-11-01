from fastapi import APIRouter

router = APIRouter(prefix="/running", tags=["Running"])

@router.get("/")
def running_status():
    return {"message": "Running router active 🏃‍♂️"}
