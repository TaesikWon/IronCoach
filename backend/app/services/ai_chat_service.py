# backend/app/services/ai_chat_service.py
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.schema.runnable import RunnableLambda
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
# ✅ LangChain이 자동으로 넘기는 stop, metadata 등을 무시하도록 수정
local_llm = RunnableLambda(lambda prompt, **kwargs: generate_response(prompt))

# ---------------------------
# 💬 대화형 체인 구성
# ---------------------------
chat_chain = ConversationalRetrievalChain.from_llm(
    llm=local_llm,
    retriever=compressed_retriever,
    memory=memory,
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
    try:
        # ✅ 최신 버전에서는 run() 대신 invoke() 사용
        result = chat_chain.invoke({"question": user_message})
        raw_output = result["answer"] if isinstance(result, dict) else result

        # ✅ GPT-4o-mini로 문체 다듬기
        refined_output = await refine_text(raw_output)

        return refined_output

    except Exception as e:
        print(f"[❌ Chat Error] {e}")
        return "죄송합니다. 코치 시스템에 일시적인 오류가 발생했습니다."
