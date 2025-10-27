// 백엔드의 /health API를 호출하는 함수
export async function checkHealth() {
  try {
    const res = await fetch("http://127.0.0.1:8000/health");
    return await res.json();
  } catch (error) {
    return { status: "error", message: "Backend not reachable ❌" };
  }
}
