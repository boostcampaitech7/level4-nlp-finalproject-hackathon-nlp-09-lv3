from pydantic import BaseModel
from typing import List

# 입력 모델
class QueryRequest(BaseModel):
    query: str

# 출력 모델
class QueryEvalResponse(BaseModel):
    context: List[str]
    answer: str

class QueryServiceResponse(BaseModel):
    answer: str
    pdfFileNames: List[str]
    audioFileNames: str
