import { useMutation, useQuery } from "@tanstack/react-query";
import { chatApi } from "../api/chatApi";
import { QueryRequest, QueryResponse } from "../types/dto/closedQueryService";

export const useClosedQueryApi = (query: string) => {
  return useQuery<QueryResponse>({
    queryKey: ["queryResult", query], // 쿼리 키 (캐싱 & 리패칭 관리)
    queryFn: () => chatApi({ query }), // API 요청 함수
    enabled: !!query, // query가 있을 때만 실행
  });
};

export const useMutateQueryApi = () => {
  return useMutation<QueryResponse, Error, QueryRequest>({
    mutationFn: chatApi, // API 요청 함수
  });
};
