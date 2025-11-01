// frontend/src/pages/ChatPage.jsx
import { useState } from "react";
import ChatMessage from "../components/ChatMessage"; // ✅ 추가
import LoadingDots from "../components/LoadingDots"; // ✅ 추가

function ChatPage() {
  const [messages, setMessages] = useState([]); // 대화 히스토리
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // 🧠 AI 서버로 메시지 전송
  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { role: "user", content: input };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      const aiMessage = { role: "assistant", content: data.reply || data.feedback };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("❌ Chat error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "⚠️ 서버 응답 오류가 발생했습니다." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // ⏎ Enter로 메시지 전송
  const handleKeyDown = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* 헤더 */}
      <header className="p-4 bg-blue-600 text-white text-lg font-semibold">
        🧠 IronCoach 대화 코칭
      </header>

      {/* 대화 영역 */}
      <main className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`p-3 rounded-2xl max-w-[70%] text-sm ${
                msg.role === "user"
                  ? "bg-blue-500 text-white rounded-br-none"
                  : "bg-white border rounded-bl-none shadow"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {/* 로딩 중 애니메이션 */}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border rounded-2xl px-3 py-2 text-gray-500">
              <span className="animate-pulse">코치가 생각 중...</span>
            </div>
          </div>
        )}
      </main>

      {/* 입력창 */}
      <footer className="p-4 border-t bg-white flex gap-2">
        <input
          type="text"
          className="flex-1 border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="메시지를 입력하세요..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 py-2 rounded-xl hover:bg-blue-600"
          disabled={loading}
        >
          전송
        </button>
      </footer>
    </div>
  );
}

export default ChatPage;
