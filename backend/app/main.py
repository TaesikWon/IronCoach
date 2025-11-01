# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routers import (
    healthcheck,
    user,
    ai_router,
    cycling,
    running,
    swimming,
    tennis,
    session_router,
)

# ✅ DB 생성
Base.metadata.create_all(bind=engine)

# ✅ FastAPI 앱 생성
app = FastAPI(title="IronCoach API")

# ✅ CORS 설정
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터 등록
app.include_router(healthcheck.router)
app.include_router(user.router)
app.include_router(ai_router.router)
app.include_router(cycling.router)
app.include_router(running.router)
app.include_router(swimming.router)
app.include_router(tennis.router)
app.include_router(session_router.router)

# ✅ 기본 경로
@app.get("/")
def root():
    return {"message": "IronCoach API is running"}
