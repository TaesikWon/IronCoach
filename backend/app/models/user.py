from sqlalchemy import Column, Integer, String
from app.core.database import Base

# SQLAlchemy 모델: 실제 DB 테이블 구조 정의
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
