# backend/app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ SQLite 데이터베이스 경로
SQLALCHEMY_DATABASE_URL = "sqlite:///./ironcoach.db"

# ✅ DB 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# ✅ 세션 로컬 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base 클래스 (모든 모델의 부모)
Base = declarative_base()


# ✅ 의존성 주입용 DB 세션 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
