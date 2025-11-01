import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

# -----------------------------
# ⚙️ 경로 설정
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "rag_data")       # ← 데이터 폴더
PERSIST_DIR = os.path.join(BASE_DIR, "vectorstore")  # ← 벡터 저장 폴더

# -----------------------------
# 🧠 임베딩 모델 설정
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# 📄 텍스트 문서 로드
# -----------------------------
docs = []
if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"❌ 데이터 폴더를 찾을 수 없습니다: {DATA_DIR}")

for file_name in os.listdir(DATA_DIR):
    if file_name.endswith(".txt"):
        file_path = os.path.join(DATA_DIR, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                docs.append(Document(page_content=content, metadata={"source": file_name}))

if not docs:
    raise ValueError("⚠️ 처리할 텍스트 파일이 없습니다.")

# -----------------------------
# 🧩 Chroma 벡터스토어 구축
# -----------------------------
db = Chroma.from_documents(
    docs,
    embedding_function=embeddings,
    persist_directory=PERSIST_DIR
)
db.persist()

print(f"✅ IronCoach RAG 데이터 구축 완료! ({len(docs)}개 문서 저장됨)")
print(f"📦 저장 경로: {PERSIST_DIR}")
