# backend/app/scripts/build_vectorstore.py
"""
IronCoach - 초기 ChromaDB 구축 스크립트
LangChain + HuggingFace Embeddings 기반
"""

import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# 1️⃣ 저장 위치 설정
VECTOR_DIR = os.path.join(os.path.dirname(__file__), "../../vectorstore")
os.makedirs(VECTOR_DIR, exist_ok=True)

# 2️⃣ 임베딩 모델 로드
print("✅ 임베딩 모델 로드 중...")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 3️⃣ 샘플 운동 데이터
sample_texts = [
    "스쿼트는 무릎을 90도로 구부리고, 무릎이 발끝보다 앞으로 나가지 않게 합니다.",
    "벤치프레스 시 어깨를 내리고, 가슴을 펴서 바벨이 가슴 중앙을 향하게 하세요.",
    "데드리프트는 허리를 곧게 유지한 채로, 엉덩이와 햄스트링의 힘으로 바벨을 들어올립니다.",
    "플랭크 자세에서는 복부에 긴장을 유지하고, 허리가 꺾이지 않게 주의하세요.",
    "런지는 한쪽 다리를 앞으로 내딛으며 무릎 각도를 90도로 유지합니다.",
    "운동 전에는 반드시 5~10분간 가벼운 스트레칭으로 워밍업하세요.",
    "세트 간 휴식은 근육 회복을 위해 1~2분 정도가 적당합니다.",
    "운동 후에는 충분한 수분 섭취와 쿨다운 스트레칭을 잊지 마세요.",
    "과도한 중량보다는 올바른 자세가 우선입니다.",
]

# 4️⃣ ChromaDB 생성
print("💾 ChromaDB 생성 중...")
db = Chroma.from_texts(sample_texts, embedding=embeddings, persist_directory=VECTOR_DIR)
db.persist()

print(f"🎉 완료! ChromaDB가 '{VECTOR_DIR}'에 생성되었습니다.")
print("샘플 데이터 개수:", len(sample_texts))
