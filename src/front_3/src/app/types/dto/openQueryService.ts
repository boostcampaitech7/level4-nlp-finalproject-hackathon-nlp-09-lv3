export interface OpenQueryRequest {
  query: string;
}

export interface OpenQueryResponse {
  answer: string;
  audioFileNames : string;
  pdfFileNames : string[];
}
