# === backend/Dockerfile ===
FROM python:3.11-slim

WORKDIR /app

# 1️⃣ 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2️⃣ 앱 코드 복사
COPY . .

# 3️⃣ 환경 변수
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# 4️⃣ FastAPI 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
