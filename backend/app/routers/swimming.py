from fastapi import APIRouter

router = APIRouter(prefix="/swimming", tags=["Swimming"])

@router.get("/")
def swimming_status():
    return {"message": "Swimming router active 🏊‍♀️"}
