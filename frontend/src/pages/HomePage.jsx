// frontend/src/pages/HomePage.jsx
import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 text-gray-800">
      <h1 className="text-4xl font-bold mb-6">🏋️‍♂️ IronCoach</h1>
      <p className="text-lg text-gray-600 mb-8">
        AI 코칭으로 당신의 훈련을 분석하고 개선하세요.
      </p>
      <div className="space-x-4">
        <Link
          to="/sessions"
          className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700"
        >
          세션 보기
        </Link>
        <Link
          to="/create-session"
          className="bg-gray-800 text-white px-6 py-3 rounded-lg hover:bg-gray-900"
        >
          새 세션 만들기
        </Link>
      </div>
    </div>
  );
}
