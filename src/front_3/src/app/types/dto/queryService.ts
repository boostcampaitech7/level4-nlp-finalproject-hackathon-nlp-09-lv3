export interface QueryRequest {
  query: string;
}

export interface QueryResponse {
  answer: string;
  audioFileNames : string;
  pdfFileNames : string[];
}
