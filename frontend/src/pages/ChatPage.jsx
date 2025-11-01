// frontend/src/pages/ChatPage.jsx
import { useState } from "react";
import axios from "axios";

export default function ChatPage() {
  const [messages, setMessages] = useState([]); // 대화 기록
  const [input, setInput] = useState(""); // 입력 메시지
  const [loading, setLoading] = useState(false);

  // 메시지 전송 함수
  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { role: "user", text: input };
    setMessages([...messages, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/ai/chat", {
        message: userMessage.text,
      });
      const coachMessage = { role: "coach", text: res.data.reply };
      setMessages((prev) => [...prev, coachMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "coach", text: "⚠️ 코치와의 연결에 문제가 발생했습니다." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // 엔터 키로 전송
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col items-center h-screen bg-gray-50 p-6">
      <h1 className="text-2xl font-bold mb-4">💬 IronCoach 대화형 코칭</h1>

      {/* 채팅창 */}
      <div className="w-full max-w-2xl bg-white shadow-md rounded-2xl p-4 flex flex-col h-[70vh] overflow-y-auto border">
        {messages.length === 0 && (
          <p className="text-gray-400 text-center mt-20">
            AI 코치에게 첫 질문을 해보세요! 🏃‍♂️
          </p>
        )}

        {messages.map((m, i) => (
          <div
            key={i}
            className={`my-2 flex ${
              m.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`px-4 py-2 rounded-2xl max-w-[75%] ${
                m.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-200 text-gray-800"
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-gray-400 text-sm text-center my-2">
            코치가 생각 중입니다 🤔...
          </div>
        )}
      </div>

      {/* 입력창 */}
      <div className="w-full max-w-2xl flex mt-4">
        <textarea
          className="flex-grow border rounded-2xl p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-400"
          rows="2"
          placeholder="메시지를 입력하세요..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="ml-2 bg-blue-500 text-white px-6 py-2 rounded-2xl hover:bg-blue-600 disabled:opacity-50"
        >
          전송
        </button>
      </div>
    </div>
  );
}
