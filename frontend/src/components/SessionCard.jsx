// frontend/src/components/SessionCard.jsx
import { Link } from "react-router-dom";
import { deleteSession } from "../api/sessionApi";

export default function SessionCard({ session, onDelete }) {
  const handleDelete = async (e) => {
    e.preventDefault(); // 링크 이동 방지
    if (confirm(`"${session.title}" 세션을 삭제하시겠습니까?`)) {
      try {
        await deleteSession(session.id);
        alert("세션이 삭제되었습니다.");
        onDelete(session.id); // 부모에서 목록 새로고침
      } catch (error) {
        console.error("세션 삭제 실패:", error);
        alert("삭제 중 오류가 발생했습니다 😢");
      }
    }
  };

  return (
    <div className="bg-white p-5 rounded-xl shadow hover:shadow-md border border-gray-100 transition relative">
      <Link to={`/sessions/${session.id}`}>
        <h3 className="text-lg font-semibold text-gray-800">{session.title}</h3>
        <p className="text-gray-600 mt-2">{session.description}</p>
        <p className="text-sm text-gray-400 mt-1">
          {new Date(session.created_at).toLocaleDateString()}
        </p>
      </Link>

      <button
        onClick={handleDelete}
        className="absolute top-3 right-3 text-red-500 hover:text-red-700"
      >
        ✕
      </button>
    </div>
  );
}
