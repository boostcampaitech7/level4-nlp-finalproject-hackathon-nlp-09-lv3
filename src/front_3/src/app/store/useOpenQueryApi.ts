import { useMutation, useQuery } from "@tanstack/react-query";
import { openDomainApi,closedDomainApi } from "../api/chatApi";
import { OpenQueryRequest, OpenQueryResponse } from "../types/dto/openQueryService";

// useMutation을 사용하여 API 요청을 처리
export const useOpenQueryApi = () => {
  return useMutation({
    mutationFn: (query: string) => openDomainApi({ query }), // mutationFn에 chatApi를 전달
    onError: (error) => {
      console.error("Mutation 에러:", error);
    },
  });
};
