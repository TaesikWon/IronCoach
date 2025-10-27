import { useEffect, useState } from "react";
import { checkHealth } from "./services/api";

function App() {
  const [status, setStatus] = useState("Loading...");

  useEffect(() => {
    checkHealth().then((data) => setStatus(data.message));
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>IronCoach 🧠</h1>
      <p>서버 상태: {status}</p>
    </div>
  );
}

export default App;
