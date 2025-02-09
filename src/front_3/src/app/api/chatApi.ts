import api from "./client"; // api 인스턴스 임포트
import { ClosedQueryRequest, ClosedQueryResponse } from "../types/dto/closedQueryService";
import { OpenQueryRequest, OpenQueryResponse } from "../types/dto/openQueryService";
import { QueryRequest, QueryResponse } from "../types/dto/queryService";

export const closedDomainApi = async ({ query }: ClosedQueryRequest): Promise<ClosedQueryResponse> => {
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

export const openDomainApi = async ({ query }: OpenQueryRequest): Promise<OpenQueryResponse> => {
  try {
    console.log("query")
    console.log(query)
    const response = await api.post("/api/for_service/query_open_domain", { query });
    console.log("response")
    console.log(response)
    return response.data;
  } catch (error) {
    // 에러 처리
    throw new Error("API 요청 실패: " + error);
  }
};

export const queryApi = async ({ query }: QueryRequest): Promise<QueryResponse> => {
  try {
    console.log("query")
    console.log(query)
    const response = await api.post("/api/for_service/query", { query });
    console.log("response")
    console.log(response)
    return response.data;
  } catch (error) {
    // 에러 처리
    throw new Error("API 요청 실패: " + error);
  }
};