# backend/app/services/ai_chat_service.py
import torch
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableLambda
from app.services.ai_service import (
    compressed_retriever,  # ✅ Chroma + CrossEncoder 리랭킹
    refine_text,            # ✅ GPT-4o-mini 문체 다듬기
    generate_response,      # ✅ Polyglot-Ko 기반 로컬 응답
)

# ---------------------------
# 🧠 대화 메모리
# ---------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# ---------------------------
# 💬 LangChain 호환용 로컬 LLM
# ---------------------------
def local_llm_fn(prompt, **kwargs):
    """
    prompt가 dict이면 'question' 키에서 가져오고, 아니면 str로 변환
    """
    text = prompt.get("question", "") if isinstance(prompt, dict) else str(prompt)
    return generate_response(text)

local_llm = RunnableLambda(local_llm_fn)

# ---------------------------
# 💬 Conversational RAG 체인 구성
# ---------------------------
chat_chain = ConversationalRetrievalChain.from_llm(
    llm=local_llm,
    retriever=compressed_retriever,
    memory=memory,
    verbose=False,
)

# ---------------------------
# 🗣️ 메인 대화 함수
# ---------------------------
async def chat_with_coach(user_message: str) -> str:
    """
    1. RAG + Polyglot-Ko 기반 로컬 LLM으로 코칭 피드백 생성
    2. GPT-4o-mini로 문체 다듬기
    """
    try:
        # (1) RAG 기반 응답 생성
        result = chat_chain.invoke({"question": user_message})
        raw_output = result["answer"] if isinstance(result, dict) else result

        # (2) GPT-4o-mini로 문체 보정
        refined_output = await refine_text(raw_output)

        return refined_output

    except Exception as e:
        print(f"[❌ Chat Error] {e}")
        return "죄송합니다. 코치 시스템에 일시적인 오류가 발생했습니다."
