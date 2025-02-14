export interface ClosedQueryRequest {
  query: string;
}

export interface ClosedQueryResponse {
  //context: string[];
  answer: string;
  audioFileNames : string;
  pdfFileNames : string[];
  visualized_name : string;
}
