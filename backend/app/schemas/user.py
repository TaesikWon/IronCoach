from pydantic import BaseModel, EmailStr

# 공통 필드
class UserBase(BaseModel):
    name: str
    email: EmailStr


# 사용자 생성 요청 시 사용
class UserCreate(UserBase):
    pass


# 사용자 응답 시 사용 (id 포함)
class User(UserBase):
    id: int

    class Config:
        orm_mode = True
