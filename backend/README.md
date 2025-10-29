# IronCoach 🧠

**AI 기반 멀티 스포츠 퍼포먼스 코칭 플랫폼**

달리기 🏃 / 수영 🏊 / 사이클 🚴 / 테니스 🎾 데이터를 분석하고 AI가 개인 맞춤 피드백을 제공하는 스마트 트레이닝 서비스입니다.

🔗 **GitHub Repository:** https://github.com/TaesikWon/IronCoach

---

## 💡 프로젝트를 만든 동기

요즘처럼 건강과 운동이 중요하게 여겨지는 시대에, 운동은 단순히 몸을 단련하는 것을 넘어 정신적 안정과 균형을 찾는 과정이 되었습니다.

특히 달리기, 수영, 사이클은 기초 체력을 기르는 대표적인 종목이며, 테니스는 집중력과 판단력을 함께 요구하는 기술형 운동으로, 신체와 정신의 밸런스를 동시에 향상시킬 수 있습니다.

이 네 가지 종목은 모두 꾸준히 수행할 때 운동 효과가 크고, 삶의 질을 높이는 데 도움이 됩니다.

그래서 저는 데이터와 AI를 활용해 운동 기록을 분석하고, 개인 맞춤형 코칭 피드백을 제공하는 서비스를 만들어보고 싶었습니다.

그 결과물이 바로 **IronCoach**입니다. 💪

---

## 📋 프로젝트 개요

IronCoach는 사용자의 운동 기록 데이터를 기반으로 통계 분석 + AI 코칭 피드백을 제공하는 개인 프로젝트입니다.

스마트워치나 운동 앱에서 내보낸 데이터를 업로드하면, AI가 기록을 분석하고 **"어떤 부분을 개선하면 좋을지"**를 코칭 형태로 알려줍니다.

---

## 🚀 주요 기능

| 기능 | 설명 |
|------|------|
| 🏃 **4종목 지원** | 달리기, 수영, 사이클, 테니스 기록 분석 |
| 📊 **데이터 분석** | pandas로 평균, 비율, 향상도 계산 |
| 💬 **AI 코칭 피드백** | LangChain + OpenAI 기반 개인 피드백 생성 |
| 🧠 **RAG 지식검색** | 운동 관련 문서에서 참고 정보를 찾아 반영 |
| 💾 **DB 관리** | SQLite로 사용자별 운동 데이터 저장 |
| 📈 **시각화 대시보드** | React + Recharts로 트렌드 시각화 |

---

## 🧩 기술 스택

| 분야 | 기술 |
|------|------|
| **Frontend** | React, Vite, TailwindCSS, Recharts |
| **Backend** | FastAPI, Python, Uvicorn |
| **Database** | SQLite |
| **AI / Data** | LangChain, OpenAI API, Pandas, ChromaDB |
| **Infra** | REST API 구조, GitHub Actions (선택) |

---

## 🗂️ 프로젝트 구조
```
ironcoach/
├── backend/
│   ├── main.py              # FastAPI 진입점
│   ├── database.py          # DB 설정
│   ├── models.py            # Record 스키마
│   ├── routers/
│   │   ├── running.py
│   │   ├── swimming.py
│   │   ├── cycling.py
│   │   └── tennis.py
│   ├── ai_coach.py          # LangChain + OpenAI 피드백 로직
│   └── knowledge_base/
│       └── training_tips.txt
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
uvicorn main:app --reload
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

## 🧠 AI 피드백 예시

**입력 데이터:**
```json
{
  "sport": "running",
  "distance": 5.0,
  "time": 27.5,
  "pace": 5.5
}
```

**AI 피드백:**
> "평균 페이스가 이전 주보다 5% 향상되었습니다. 꾸준한 훈련이 잘 유지되고 있습니다. 다음 목표는 10km 구간에서 동일한 페이스를 유지하는 것입니다."

---

## 📅 개발 단계

| 단계 | 목표 | 상태 |
|------|------|------|
| **MVP** | 4종목 분석 + AI 피드백 | ✅ 완료 |
| **Phase 2** | 골프 등 신규 종목 추가 | 🔜 예정 |
| **Phase 3** | 맞춤형 훈련 플랜 추천 | 🔜 예정 |

---

## 👨‍💻 개발자

**Taesik Won**

- Backend & AI Developer
- Focus: Generative AI, NLP, Data Engineering
- GitHub: [@TaesikWon](https://github.com/TaesikWon)

---

## 📜 라이선스

본 프로젝트는 개인 포트폴리오 및 학습 목적으로 제작되었습니다.
```
Copyright (c) 2025 Taesik Won. All Rights Reserved.
```

- 코드 열람 및 학습 목적 참고는 자유롭게 가능합니다.
- 상업적 이용, 무단 복제 및 재배포는 금지됩니다.