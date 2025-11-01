# IronCoach

**AI 기반 멀티 스포츠 퍼포먼스 코칭 플랫폼**

달리기 🏃 / 수영 🏊 / 사이클 🚴 / 테니스 🎾 데이터를 분석하고  
AI가 개인 맞춤 피드백을 제공하는 스마트 트레이닝 서비스입니다.

---

## 💡 프로젝트를 만든 동기

요즘처럼 건강과 운동이 중요하게 여겨지는 시대에,  
운동은 단순히 몸을 단련하는 것을 넘어 **정신적 안정과 균형**을 찾는 과정이 되었습니다.

특히 **달리기, 수영, 사이클**은 기초 체력을 기르는 대표적인 종목이며,  
**테니스**는 집중력과 판단력을 함께 요구하는 기술형 운동으로,  
신체와 정신의 밸런스를 동시에 향상시킬 수 있습니다.

이 네 가지 종목은 모두 꾸준히 수행할 때 운동 효과가 크고, 삶의 질을 높이는 데 도움이 됩니다.  

그래서 저는 **데이터와 AI를 활용해 운동 기록을 분석**하고,  
**개인 맞춤형 코칭 피드백**을 제공하는 서비스를 만들어보고 싶었습니다.

그 결과물이 바로 **IronCoach**입니다. 💪

---

## 📋 프로젝트 개요

IronCoach는 사용자의 운동 기록 데이터를 기반으로  
**통계 분석 + AI 코칭 피드백**을 제공하는 개인 프로젝트입니다.

스마트워치나 운동 앱에서 내보낸 데이터를 업로드하면,  
AI가 기록을 분석하고 **"어떤 부분을 개선하면 좋을지"**를 코칭 형태로 알려줍니다.

---

## 🚀 주요 기능

| 기능 | 설명 |
|------|------|
| 🏃 **4종목 지원** | 달리기, 수영, 사이클, 테니스 기록 분석 |
| 📊 **데이터 분석** | pandas로 평균, 비율, 향상도 계산 |
| 💬 **AI 코칭 피드백** | GPT2(로컬) + GPT-4o-mini(OpenAI) 기반 피드백 생성 |
| 🧠 **RAG 지식검색** | ChromaDB + CrossEncoder 기반 문서 검색 및 리랭킹 |
| 💾 **DB 관리** | SQLite 또는 PostgreSQL에 사용자별 피드백 저장 |
| 📈 **시각화 대시보드** | React + Recharts로 훈련 트렌드 시각화 |

---

## 🧩 기술 스택

| 분야 | 기술 |
|------|------|
| **Frontend** | React, Vite, TailwindCSS, Recharts |
| **Backend** | FastAPI, Python, Uvicorn |
| **Database** | SQLite / PostgreSQL |
| **AI / Data** | LangChain, HuggingFace, ChromaDB, OpenAI API, SentenceTransformers |
| **LLM** | GPT2 (로컬 테스트용), GPT-4o-mini (Refine 단계) |
| **Infra** | REST API 구조, .env 환경변수 기반 설정 |

---

## 🗂️ 프로젝트 구조
```
ironcoach/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI 진입점
│   │   ├── core/
│   │   │   ├── config.py           # 환경 변수 관리
│   │   │   └── db.py               # DB 세션 관리
│   │   ├── models/
│   │   │   └── session.py          # Feedback ORM 모델
│   │   ├── routers/
│   │   │   └── ai_router.py        # AI 피드백 관련 API 엔드포인트
│   │   └── services/
│   │       └── ai_service.py       # LangChain + GPT2 + RAG 피드백 로직
│   ├── vectorstore/                # RAG용 문서 임베딩 DB (Chroma)
│   ├── models/ironcoach-llm/       # 로컬 LLM (선택)
│   └── data_preprocess.py          # 테스트용 RAG 데이터 생성 스크립트
│
└── frontend/
    ├── src/
    │   ├── pages/
    │   │   ├── UploadPage.jsx
    │   │   ├── StatsPage.jsx
    │   │   └── FeedbackPage.jsx
    │   ├── components/
    │   ├── api/
    │   └── App.jsx
    └── package.json
```

---

## ⚙️ 실행 방법

### 1️⃣ 백엔드 실행
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2️⃣ 프론트엔드 실행
```bash
cd frontend
npm install
npm run dev
```

### 3️⃣ 브라우저에서 확인
```
http://localhost:5173
```

---

## 📚 RAG 데이터 구축

AI 피드백을 위한 문서 검색(RAG)을 활성화하려면,  
`backend/data_preprocess.py`를 실행해 테스트용 데이터를 생성하세요.
```bash
python backend/data_preprocess.py
```

**예시 데이터 폴더 구조:**
```
vectorstore/
├── running_tips.txt
├── swimming_tips.txt
├── cycling_tips.txt
├── tennis_tips.txt
└── recovery_tips.txt
```

---

## 🧠 AI 피드백 예시

### 입력 데이터
```json
{
  "sport": "running",
  "distance": 5.0,
  "time": 27.5,
  "pace": 5.5
}
```

### AI 피드백
```
"평균 페이스가 이전 주보다 5% 향상되었습니다.
후반부 페이스 유지력이 좋아졌습니다.
다음 주는 10km 구간에서 동일한 리듬을 유지하는 것을 목표로 해보세요."
```

---

## 📅 개발 단계

| 단계 | 목표 | 상태 |
|------|------|------|
| **MVP** | 4종목 분석 + AI 피드백 | ✅ 완료 |
| **Phase 2** | RAG 기반 문서 추천 고도화 | 🚧 진행 중 |
| **Phase 3** | 맞춤형 훈련 플랜 추천 | 🔜 예정 |

---

## 👨‍💻 개발자

**Taesik Won**

- Backend & AI Developer
- Focus: Generative AI, NLP, Data Engineering
- GitHub: [@TaesikWon](https://github.com/TaesikWon)

---

## 📜 라이선스

**🔒 IronCoach Custom License (All Rights Reserved)**

이 프로젝트는 개인 포트폴리오 및 학습용으로 제작되었습니다.  
다음의 조건에 따라 제한적으로 열람만 허용됩니다.

### ✅ 허용되는 범위

- 개인 학습 및 참고 목적의 열람
- 포트폴리오 또는 기술 참고를 위한 비상업적 이용

### ❌ 금지되는 행위

- 코드의 수정, 복제, 재배포, 포크(Fork)
- 코드 일부 또는 전체를 상업적 제품 / 서비스 / 강의 / 콘텐츠에 사용하는 행위

### ⚠️ 저작권 안내
```
Copyright (c) 2025 Taesik Won
All Rights Reserved.

본 저장소의 소스 코드, 문서, 디자인, 데이터 구조는
저작권법에 의해 보호되며, 저작자의 서면 동의 없이 사용할 수 없습니다.
```