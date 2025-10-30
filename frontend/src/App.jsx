// frontend/src/App.jsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import SessionsPage from "./pages/SessionsPage";
import SessionPage from "./pages/SessionPage";
import CreateSessionPage from "./pages/CreateSessionPage";
import "./index.css"; // ✅ Tailwind 포함

function App() {
  return (
    <Router>
      <Routes>
        {/* 🏠 홈 */}
        <Route path="/" element={<HomePage />} />

        {/* 📋 세션 목록 */}
        <Route path="/sessions" element={<SessionsPage />} />

        {/* 🔍 단일 세션 상세 */}
        <Route path="/sessions/:id" element={<SessionPage />} />

        {/* 🆕 세션 생성 */}
        <Route path="/create-session" element={<CreateSessionPage />} />
      </Routes>
    </Router>
  );
}

export default App;
