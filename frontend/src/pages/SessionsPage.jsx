// frontend/src/pages/SessionsPage.jsx
import { useEffect, useState } from "react";
import { getSessions } from "../api/sessionApi";
import SessionCard from "../components/SessionCard";

export default function SessionsPage() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // 세션 목록 불러오기
  const fetchSessions = async () => {
    try {
      const data = await getSessions();
      setSessions(data);
    } catch (err) {
      console.error("세션 목록 불러오기 실패:", err);
      setError("서버에서 세션 데이터를 불러오지 못했습니다 😢");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  // 세션 삭제 후 목록에서 제거
  const handleDelete = (id) => {
    setSessions((prev) => prev.filter((s) => s.id !== id));
  };

  if (loading) return <p className="p-8 text-gray-500">로딩 중...</p>;
  if (error) return <p className="p-8 text-red-500">{error}</p>;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">🏋️ 세션 목록</h1>

      {sessions.length === 0 ? (
        <p className="text-gray-500">등록된 세션이 없습니다.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {sessions.map((s) => (
            <SessionCard key={s.id} session={s} onDelete={handleDelete} />
          ))}
        </div>
      )}
    </div>
  );
}
