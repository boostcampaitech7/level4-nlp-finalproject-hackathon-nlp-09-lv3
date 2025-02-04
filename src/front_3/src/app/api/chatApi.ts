import api from "./client"; // api 인스턴스 임포트
import { ClosedQueryRequest, ClosedQueryResponse } from "../types/dto/closedQueryService";

export const chatApi = async ({ query }: ClosedQueryRequest): Promise<ClosedQueryResponse> => {
  try {
    console.log("query")
    console.log(query)
    const response = await api.post("/api/for_service/query_closed_domain", { query });
    console.log("response")
    console.log(response)
    return response.data;
  } catch (error) {
    // 에러 처리
    throw new Error("API 요청 실패: " + error);
  }
};