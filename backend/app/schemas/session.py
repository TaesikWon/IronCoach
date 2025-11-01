# app/schemas/session.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ✅ 기본 스키마 (공통 필드)
class SessionBase(BaseModel):
    title: str
    user_id: int   # 어떤 사용자의 세션인지 연결

# ✅ 세션 생성 시 요청용 (Create)
class SessionCreate(SessionBase):
    pass

# ✅ 세션 수정 시 요청용 (Update)
class SessionUpdate(BaseModel):
    title: Optional[str] = None

# ✅ 세션 응답용 (Response)
class SessionResponse(SessionBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
