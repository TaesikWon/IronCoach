from fastapi import APIRouter

router = APIRouter(prefix="/cycling", tags=["Cycling"])

@router.get("/")
def cycling_status():
    return {"message": "Cycling router active"}
