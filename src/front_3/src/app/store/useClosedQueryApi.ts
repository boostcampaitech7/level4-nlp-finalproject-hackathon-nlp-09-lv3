import { useMutation, useQuery } from "@tanstack/react-query";
import { chatApi } from "../api/chatApi";
import { ClosedQueryRequest, ClosedQueryResponse } from "../types/dto/closedQueryService";

// 쿼리 요청을 처리하는 hook
export const useClosedQueryApi = (query: string) => {
  console.log("useClosedQueryApi");
  return useQuery<ClosedQueryResponse>({
    queryKey: ["queryResult", query], // 쿼리 키 (캐싱 & 리패칭 관리)
    queryFn: () => chatApi({ query }), // API 요청 함수
    enabled: !!query, // query가 있을 때만 실행
  });
};

// 뮤테이션 요청을 처리하는 hook
export const useMutateQueryApi = () => {
  return useMutation<ClosedQueryResponse, Error, ClosedQueryRequest>({
    mutationFn: chatApi, // API 요청 함수
  });
};
