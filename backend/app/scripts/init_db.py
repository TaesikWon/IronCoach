app/scripts/init_db.py
from app.core.db import Base, engine
from app.models import session

print("📦 PostgreSQL 테이블 생성 중...")
Base.metadata.create_all(bind=engine)
print("✅ 완료! sessions, feedbacks 테이블이 생성되었습니다.")
