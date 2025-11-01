# app/crud/session_crud.py

from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.schemas.session import SessionCreate, SessionUpdate


# ✅ CREATE (세션 생성)
def create_session(db: Session, session_data: SessionCreate):
    new_session = SessionModel(
        title=session_data.title,
        user_id=session_data.user_id
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session


# ✅ READ (모든 세션 조회)
def get_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SessionModel).offset(skip).limit(limit).all()


# ✅ READ (특정 세션 조회)
def get_session_by_id(db: Session, session_id: int):
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()


# ✅ UPDATE (세션 수정)
def update_session(db: Session, session_id: int, update_data: SessionUpdate):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        return None

    # 수정할 데이터가 존재하는 경우에만 업데이트
    if update_data.title is not None:
        db_session.title = update_data.title

    db.commit()
    db.refresh(db_session)
    return db_session


# ✅ DELETE (세션 삭제)
def delete_session(db: Session, session_id: int):
    db_session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not db_session:
        return None

    db.delete(db_session)
    db.commit()
    return db_session
