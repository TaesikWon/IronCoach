// frontend/src/components/ChatMessage.jsx

// 💬 말풍선 전용 컴포넌트
export default function ChatMessage({ role, content }) {
  const isUser = role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`p-3 rounded-2xl max-w-[70%] text-sm leading-relaxed break-words ${
          isUser
            ? "bg-blue-500 text-white rounded-br-none"
            : "bg-white border rounded-bl-none shadow"
        }`}
      >
        {content}
      </div>
    </div>
  );
}
