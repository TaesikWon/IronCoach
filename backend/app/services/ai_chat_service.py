# backend/app/services/ai_chat_service.py
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableLambda  # ✅ 추가
from app.services.ai_service import (
    compressed_retriever,   # RAG 기반 문서 검색기
    refine_text,            # GPT-4o-mini 문체 다듬기
    generate_response,      # GPT2 로컬 응답 함수
)

# ---------------------------
# 🧠 대화 메모리 (세션별 대화 기억)
# ---------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# ---------------------------
# 💬 로컬 LLM (GPT2 기반)
# ---------------------------
local_llm = RunnableLambda(lambda prompt: generate_response(prompt))

# ---------------------------
# 💬 대화형 체인 구성
# ---------------------------
chat_chain = ConversationalRetrievalChain.from_llm(
    llm=local_llm,                  # ✅ LocalLLMWrapper 대신 RunnableLambda 사용
    retriever=compressed_retriever, # ✅ RAG + 리랭킹
    memory=memory,                  # ✅ 대화 기록 저장
    verbose=False
)

# ---------------------------
# 🗣️ 메인 함수
# ---------------------------
async def chat_with_coach(user_message: str) -> str:
    """
    사용자의 메시지를 받아 RAG + LLM을 통해
    AI 코치의 자연스러운 응답을 생성합니다.
    """
    # 1️⃣ RAG + GPT2 기반 1차 응답 생성
    raw_output = chat_chain.run(user_message)

    # 2️⃣ GPT-4o-mini로 문체 다듬기 (비동기)
    refined_output = await refine_text(raw_output)

    # 3️⃣ 최종 응답 반환
    return refined_output
