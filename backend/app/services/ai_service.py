# app/services/ai_service.py
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from transformers import AutoModelForCausalLM, AutoTokenizer
from openai import AsyncOpenAI
from app.core.config import settings
from app.core.db import SessionLocal
from app.models.session import Feedback
import torch

# 내부 모델 로드
tokenizer = AutoTokenizer.from_pretrained("./models/ironcoach-llm")
model = AutoModelForCausalLM.from_pretrained("./models/ironcoach-llm")

def generate_response(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ChromaDB 설정
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="vectorstore", embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""당신은 전문 트레이너입니다.
아래 세션 기록(context)을 참고하여 피드백을 제공합니다.

[세션 기록]
{context}

[질문]
{question}

1. 훈련 강도 평가
2. 자세 및 효율 개선 팁
3. 다음 훈련 제안
""",
)

class LocalLLMWrapper:
    def __call__(self, prompt: str):
        return generate_response(prompt)

qa_chain = RetrievalQA.from_chain_type(
    llm=LocalLLMWrapper(),
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
)

client = AsyncOpenAI(api_key=settings.openai_api_key)

async def refine_text(text: str) -> str:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "운동 코칭 피드백을 자연스럽게 다듬어 주세요."},
            {"role": "user", "content": text},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()

# 최종 분석
async def analyze_training_session(title: str, description: str, session_id: int):
    query = f"{title}\n{description}"
    raw_output = qa_chain.run(query)
    refined_output = await refine_text(raw_output)

    # 결과를 PostgreSQL에 저장
    db_session = SessionLocal()
    feedback = Feedback(session_id=session_id, ai_feedback=refined_output)
    db_session.add(feedback)
    db_session.commit()
    db_session.close()

    return refined_output
