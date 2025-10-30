// frontend/src/pages/SessionPage.jsx
import { useNavigate, useParams, Link } from "react-router-dom";
import { getSessionById, deleteSession } from "../api/sessionApi";
import { useEffect, useState } from "react";

export default function SessionPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getSessionById(id)
      .then(setSession)
      .catch(() => setError("세션 정보를 불러오지 못했습니다 😢"));
  }, [id]);

  const handleDelete = async () => {
    if (confirm("이 세션을 삭제하시겠습니까?")) {
      try {
        await deleteSession(id);
        alert("세션이 삭제되었습니다.");
        navigate("/sessions"); // 삭제 후 목록으로 이동
      } catch (err) {
        console.error("삭제 실패:", err);
        alert("삭제 중 오류가 발생했습니다 😢");
      }
    }
  };

  if (error) return <p className="p-8 text-red-500">{error}</p>;
  if (!session) return <p className="p-8 text-gray-500">로딩 중...</p>;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-4">
        <Link to="/sessions" className="text-blue-600 hover:underline text-sm">
          ← 세션 목록으로
        </Link>
        <button
          onClick={handleDelete}
          className="text-red-500 hover:underline text-sm"
        >
          삭제
        </button>
      </div>

      <h1 className="text-3xl font-bold mb-4">{session.title}</h1>
      <p className="text-gray-600 mb-2">{session.description}</p>
      <p className="text-gray-400 text-sm">
        생성일:{" "}
        {session.created_at
          ? new Date(session.created_at).toLocaleDateString()
          : "정보 없음"}
      </p>
    </div>
  );
}
