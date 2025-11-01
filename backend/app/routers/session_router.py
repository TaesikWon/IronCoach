# app/routers/session_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse
from app.crud import session_crud

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)

# ✅ CREATE: 세션 생성
@router.post("/", response_model=SessionResponse)
def create_session(session_data: SessionCreate, db: Session = Depends(get_db)):
    return session_crud.create_session(db, session_data)

# ✅ READ: 모든 세션 조회
@router.get("/", response_model=List[SessionResponse])
def get_all_sessions(db: Session = Depends(get_db)):
    return session_crud.get_sessions(db)

# ✅ READ: 특정 세션 조회
@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    db_session = session_crud.get_session_by_id(db, session_id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session

# ✅ UPDATE: 세션 수정
@router.put("/{session_id}", response_model=SessionResponse)
def update_session(session_id: int, session_data: SessionUpdate, db: Session = Depends(get_db)):
    updated = session_crud.update_session(db, session_id, session_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Session not found")
    return updated

# ✅ DELETE: 세션 삭제
@router.delete("/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    deleted = session_crud.delete_session(db, session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": f"Session {session_id} deleted successfully"}
