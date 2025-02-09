import { useMutation, useQuery } from "@tanstack/react-query";
import { openDomainApi,closedDomainApi } from "../api/chatApi";
import { ClosedQueryRequest, ClosedQueryResponse } from "../types/dto/closedQueryService";

// 쿼리 요청을 처리하는 hook
// export const useClosedQueryApi = (query: string) => {
//   console.log("useClosedQueryApi");
//   return useQuery<ClosedQueryResponse>({
//     queryKey: ["queryResult", query], // 쿼리 키 (캐싱 & 리패칭 관리)
//     queryFn: () => chatApi({ query }), // API 요청 함수
//     enabled: !!query, // query가 있을 때만 실행
//   });
// };

// useMutation을 사용하여 API 요청을 처리
export const useClosedQueryApi = () => {
  return useMutation({
    mutationFn: (query: string) => closedDomainApi({ query }), // mutationFn에 chatApi를 전달
    onError: (error) => {
      console.error("Mutation 에러:", error);
    },
  });
};

// interface ChatApiRequest {
//   query: string;
// }

// interface ChatApiResponse {
//   answer: string;
//   context?: string;
// }

// const mockChatApi = async (request: ChatApiRequest): Promise<ChatApiResponse> => {
//   // 실제 API 호출 대신 지연을 주어 응답을 모사
//   await new Promise(resolve => setTimeout(resolve, 1000));
  
//   return {
//     answer: `이것은 "${request.query}"에 대한 테스트 응답입니다.`,
//     context: "테스트 문서"
//   };
// };

// 뮤테이션 요청을 처리하는 hook
// export const useMutateQueryApi = () => {
//   return useMutation({
//     mutationFn: mockChatApi,
//     onError: (error) => {
//       console.error('Mutation 에러:', error);
//     },
//   });
// };
