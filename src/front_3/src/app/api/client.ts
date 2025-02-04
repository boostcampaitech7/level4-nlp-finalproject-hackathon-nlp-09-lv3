import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // 기본 URL 설정
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;