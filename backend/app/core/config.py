# backend/app/core/config.py
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    # === App Info ===
    app_name: str = "IronCoach"
    app_env: str = "development"
    app_port: int = 8000

    # === Database ===
    database_url: str | None = None

    # === OpenAI / API Keys ===
    openai_api_key: str | None = None

    # === Vector DB ===
    vector_db_path: str = "./backend/vectorstore"

    # === Environment ===
    environment: str = "development"

    # === Config ===
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

# 전역 인스턴스
settings = Settings()

# 로드 확인용 (선택)
if __name__ == "__main__":
    print(f"✅ Loaded settings from: {ENV_PATH}")
    print(f"APP_ENV: {settings.app_env}")
    print(f"DB_URL: {settings.database_url}")
    print(f"VECTOR_DB_PATH: {settings.vector_db_path}")
