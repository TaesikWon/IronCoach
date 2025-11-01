// frontend/src/pages/CreateSessionPage.jsx
import { useState } from "react";
import { createSession, analyzeSession } from "../api/sessionApi";
import { useNavigate } from "react-router-dom";

export default function CreateSessionPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ title: "", description: "" });
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [feedback, setFeedback] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // ✅ 세션 생성
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await createSession(form);
      alert("세션이 성공적으로 생성되었습니다!");
      navigate("/sessions");
    } catch (error) {
      console.error("세션 생성 실패:", error);
      alert("세션 생성 중 오류가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setLoading(false);
    }
  };

  // ✅ AI 분석 요청
  const handleAIAnalyze = async () => {
    setAnalyzing(true);
    try {
      const result = await analyzeSession(form);
      setFeedback(result.feedback);
    } catch (error) {
      console.error("AI 피드백 실패:", error);
      alert("AI 분석 중 오류가 발생했습니다.");
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-8">
      <h2 className="text-2xl font-bold mb-6">🆕 새 세션 추가</h2>

      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-xl shadow-md w-full max-w-md space-y-4"
      >
        <input
          type="text"
          name="title"
          placeholder="세션 제목"
          value={form.title}
          onChange={handleChange}
          required
          className="w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-blue-500"
        />
        <textarea
          name="description"
          placeholder="세션 설명"
          value={form.description}
          onChange={handleChange}
          required
          className="w-full border border-gray-300 rounded-lg p-2 h-32 focus:ring-2 focus:ring-blue-500"
        />

        {/* ✅ AI 피드백 버튼 */}
        <button
          type="button"
          onClick={handleAIAnalyze}
          disabled={analyzing}
          className={`w-full py-2 rounded-lg text-white transition ${
            analyzing
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-green-600 hover:bg-green-700"
          }`}
        >
          {analyzing ? "분석 중..." : "AI 피드백 받기"}
        </button>

        {/* ✅ 생성 버튼 */}
        <button
          type="submit"
          disabled={loading}
          className={`w-full text-white py-2 rounded-lg transition ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          }`}
        >
          {loading ? "생성 중..." : "세션 생성"}
        </button>
      </form>

      {/* ✅ 분석 결과 표시 */}
      {feedback && (
        <div className="mt-6 bg-white p-4 rounded-lg shadow w-full max-w-md">
          <h3 className="font-semibold mb-2">AI 피드백 💬</h3>
          <p className="text-gray-700 whitespace-pre-line">{feedback}</p>
        </div>
      )}
    </div>
  );
}
