# backend/app/services/ai_service.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from sentence_transformers import CrossEncoder
from langchain.schema.runnable import RunnableLambda
from openai import AsyncOpenAI
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.session import Feedback

# ---------------------------
# 🧠 Polyglot-Ko-1.3B 로컬 모델 로드
# ---------------------------
print("🔹 Polyglot-Ko-1.3B 모델 로드 중...")
model_id = "EleutherAI/polyglot-ko-1.3b"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto"
)

def generate_response(prompt: str) -> str:
    """Polyglot-Ko-1.3B 기반 로컬 LLM 응답 생성"""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# ---------------------------
# 🧩 ChromaDB + 리랭킹 설정
# ---------------------------
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="vectorstore", embedding_function=embeddings)
retriever = db.as_retriever(search_kwargs={"k": 10})

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
reranker = CrossEncoderReranker.construct(model=cross_encoder, top_n=3)

compressed_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    base_compressor=reranker
)

# ---------------------------
# 💬 프롬프트 템플릿
# ---------------------------
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""당신은 전문 트레이너입니다.
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
# 🧠 LLM 래퍼
# ---------------------------
def local_llm(prompt: str) -> str:
    return generate_response(prompt)

LocalLLM = RunnableLambda(local_llm)

# ---------------------------
# 💬 RetrievalQA 체인 구성
# ---------------------------
qa_chain = RetrievalQA.from_chain_type(
    llm=LocalLLM,
    chain_type="stuff",
    retriever=compressed_retriever,
    chain_type_kwargs={"prompt": prompt},
)

# ---------------------------
# 🪄 GPT-4o-mini 문체 다듬기
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
# 🧩 최종 분석 + DB 저장
# ---------------------------
async def analyze_training_session(title: str, description: str, session_id: int):
    """
    1️⃣ Polyglot-Ko 기반 로컬 LLM + RAG로 세션 분석
    2️⃣ GPT-4o-mini로 문체 다듬기
    3️⃣ PostgreSQL/SQLite에 피드백 저장
    """
    query = f"{title}\n{description}"
    raw_output = qa_chain.run(query)
    refined_output = await refine_text(raw_output)

    db_session = SessionLocal()
    try:
        feedback = Feedback(session_id=session_id, ai_feedback=refined_output)
        db_session.add(feedback)
        db_session.commit()
    finally:
        db_session.close()

    return refined_output
