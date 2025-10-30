// frontend/src/api/sessionApi.js
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000"; // FastAPI 서버 주소

// ✅ 공통 axios 인스턴스
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

// ✅ 세션 목록 가져오기
export const getSessions = async () => {
  try {
    const response = await api.get("/sessions");
    return response.data; // FastAPI가 리스트를 바로 반환한다고 가정
  } catch (error) {
    console.error("세션 목록 불러오기 실패:", error);
    throw new Error("세션 데이터를 불러오지 못했습니다.");
  }
};

// ✅ 단일 세션 상세 조회
export const getSessionById = async (id) => {
  try {
    const response = await api.get(`/sessions/${id}`);
    return response.data;
  } catch (error) {
    console.error(`세션 ${id} 조회 실패:`, error);
    throw new Error("세션 정보를 불러오지 못했습니다.");
  }
};

// ✅ 새 세션 생성
export const createSession = async (data) => {
  try {
    const response = await api.post("/sessions", data);
    return response.data;
  } catch (error) {
    console.error("세션 생성 실패:", error);
    throw new Error("세션을 생성하지 못했습니다.");
  }
};

// ✅ 세션 삭제
export const deleteSession = async (id) => {
  try {
    await api.delete(`/sessions/${id}`); // FastAPI가 204 No Content 반환 가정
    return true;
  } catch (error) {
    console.error(`세션 ${id} 삭제 실패:`, error);
    throw new Error("세션을 삭제하지 못했습니다.");
  }
};

// ✅ AI 세션 분석
export const analyzeSession = async (data) => {
  try {
    const response = await api.post("/ai/analyze", data);
    return response.data;
  } catch (error) {
    console.error("AI 분석 실패:", error);
    throw new Error("AI 분석 요청 중 오류가 발생했습니다.");
  }
};
