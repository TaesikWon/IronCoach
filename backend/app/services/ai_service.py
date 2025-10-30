from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def analyze_training_session(title: str, description: str) -> str:
    prompt = f"""
    운동 세션 분석 요청:
    제목: {title}
    설명: {description}

    AI 코치로서 피드백을 다음 형식으로 제공해 주세요:
    - 훈련 강도 평가
    - 자세 및 효율 개선 팁
    - 다음 훈련 제안
    """

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
