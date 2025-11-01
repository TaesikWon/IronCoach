import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from sentence_transformers import CrossEncoder
from openai import AsyncOpenAI
from app.core.config import settings
from app.core.db import SessionLocal
from app.models.session import Feedback

# ---------------------------
# 🧠 테스트용 GPT2 모델 로드
# ---------------------------
print("🤖 GPT2 모델 로드 중...")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

def generate_response(prompt: str) -> str:
    """GPT2 모델을 이용해 로컬에서 간단한 응답 생성"""
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ---------------------------
# 🧩 ChromaDB + 리랭킹 설정
# ---------------------------
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="vectorstore", embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 10})

# 🔥 CrossEncoder 기반 리랭커 (버그 회피용 안전 초기화)
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# ✅ 최신 LangChain(0.3.5)에서는 construct()로 타입 검증 회피
reranker = CrossEncoderReranker.construct(
    model=cross_encoder,
    top_n=3
)

compressed_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=reranker
)

# ---------------------------
# 💬 프롬프트 템플릿
# ---------------------------
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
당신은 전문 트레이너입니다.
아래의 세션 기록(context)을 참고하여 피드백을 제공합니다.

[세션 기록]
{context}

[질문]
{question}

1. 훈련 강도 평가
2. 자세 및 효율 개선 팁
3. 다음 훈련 제안
""",
)

# ---------------------------
# 🧠 LLM 래퍼 (LangChain 호환용)
# ---------------------------
class LocalLLMWrapper:
    def __call__(self, prompt: str):
        return generate_response(prompt)

qa_chain = RetrievalQA.from_chain_type(
    llm=LocalLLMWrapper(),
    chain_type="stuff",
    retriever=compressed_retriever,  # ✅ 리랭킹 반영
    chain_type_kwargs={"prompt": prompt},
)

# ---------------------------
# 🪄 GPT로 문체 다듬기
# ---------------------------
client = AsyncOpenAI(api_key=settings.openai_api_key)

async def refine_text(text: str) -> str:
    """OpenAI GPT 모델로 문체 자연스럽게 보정"""
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "운동 코칭 피드백을 자연스럽게 다듬어 주세요."},
            {"role": "user", "content": text},
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content.strip()

# ---------------------------
# 🧩 최종 분석 + PostgreSQL 저장
# ---------------------------
async def analyze_training_session(title: str, description: str, session_id: int):
    """세션 데이터를 분석하고 AI 피드백을 생성 후 DB 저장"""
    query = f"{title}\n{description}"
    raw_output = qa_chain.run(query)
    refined_output = await refine_text(raw_output)

    db_session = SessionLocal()
    feedback = Feedback(session_id=session_id, ai_feedback=refined_output)
    db_session.add(feedback)
    db_session.commit()
    db_session.close()

    return refined_output
