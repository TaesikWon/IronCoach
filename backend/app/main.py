from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, healthcheck, ai_feedback, cycling, running, swimming, tennis
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS 설정
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
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
app.include_router(ai_feedback.router)
app.include_router(cycling.router)
app.include_router(running.router)
app.include_router(swimming.router)
app.include_router(tennis.router)

@app.get("/")
def root():
    return {"message": "IronCoach API is running 🚀"}
