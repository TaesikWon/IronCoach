# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    database_url: str | None = None
    environment: str = "development"

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()
