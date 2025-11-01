export default function ChatMessage({ role, content }) {
  const isUser = role === "user";
  const time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  return (
    <div className={`flex items-end mb-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {/* 말풍선 */}
      <div
        className={`max-w-[70%] px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-sm ${
          isUser
            ? "bg-blue-500 text-white rounded-br-none"
            : "bg-white border border-gray-200 rounded-bl-none"
        }`}
      >
        <p>{content}</p>
        <p
          className={`text-[10px] mt-1 ${
            isUser ? "text-blue-100 text-right" : "text-gray-400 text-left"
          }`}
        >
          {time}
        </p>
      </div>
    </div>
  );
}
