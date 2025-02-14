import { useMutation, useQuery } from "@tanstack/react-query";
import { queryApi } from "../api/chatApi";
import { QueryRequest, QueryResponse } from "../types/dto/queryService";

// useMutation을 사용하여 API 요청을 처리
export const useQueryApi = () => {
  return useMutation({
    mutationFn: (query: string) => queryApi({ query }), // mutationFn에 chatApi를 전달
    onError: (error) => {
      console.error("Mutation 에러:", error);
    },
  });
};


