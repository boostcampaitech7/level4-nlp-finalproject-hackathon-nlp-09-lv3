import api from "./client";
import { ClosedQueryRequest, ClosedQueryResponse } from "../types/dto/closedQueryService";

export const chatApi = async (query: string): Promise<ClosedQueryResponse> => {
    const requestBody: ClosedQueryRequest = { query };
    const response = await api.post<ClosedQueryResponse>("/api/for_service/query_closed_domain", requestBody);
    return response.data;
  };