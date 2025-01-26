from retrievals.BM25_retrieval import BM25Search
from retrievals.Dense_passage_retrieval import DPRRetriever
from retrievals.Ensemble_retrieval import ensemble_retrieval
from dotenv import load_dotenv
import os
from openai import OpenAI
from pydantic import BaseModel
load_dotenv()


# class CalendarEvent(BaseModel):
#     name: str
#     date: str
#     participants: list[str]

class LLM_Retriever:
    def __init__(self, documents, db, topk1 = 10, topk2=5):
        bm25 = BM25Search().bm25_retriever(documents, topk = topk1)
        dpr = DPRRetriever(db = db, topk = topk1)
        retrievals = [bm25, dpr]
        weights = [0.5, 0.5]
        search_type = 'mmr'
        self.topk2 = topk2
        self.ensemble = ensemble_retrieval(retrievals, topk = topk1, weights = weights, search_type = search_type)

    
    def invoke(self, query):
        topk2 = self.topk2
        # Retrieval 수행
        retrieval_results = self.ensemble.invoke(query)
        docs = str([doc.metadata['original_content'] for doc in retrieval_results])
        
        # OpenAI API 키 로드
        api_key = os.environ['OPENAI_API_KEY']
        client = OpenAI(api_key=api_key)
        
        # GPT-4o 모델에 사용할 프롬프트 생성
        prompts = f"""다음 주어지는 문서들 중 질문에 가장 도움이 되는 문서의 인덱스 {topk2}가지를 평가 기준을 반드시 준수하여 출력하세요.
         [평가 기준]
                1. **Do any of the retrieved contexts show strong similarity to the Ground Truth?** (5 points)  
                [Yes/No]

                2. **Do the retrieved contexts collectively capture essential information from the Ground Truth?** (5 points)  
                [Yes/No]

                3. **Do the retrieved contexts sufficiently address the user’s question?** (4 points)  
                [Yes/No]

                4. **Are all retrieved contexts relevant to the Ground Truth or the user’s query?** (3 points)  
                [Yes/No]

                5. **Does the combined length and number of retrieved contexts remain reasonable without overwhelming the user with excessive or irrelevant details?** (3 points)  
                [Yes/No]
         [예시]
          문서들: [문서1, 문서2, 문서3....]
          출력: 주어진 문서 중 가장 평가 기준에 부합하는 도움이 되는 문서 {topk2}개의 인덱스 (0,3,5,8,9 처럼)
          답변은 반드시 인덱스만 내보내세요.
          """

        # OpenAI GPT 호출
        while True:
            try:
                completion = client.chat.completions.create(
                model='gpt-4o-2024-08-06',
                messages=[
                    {"role": "system", "content": prompts},
                    {"role": "user", "content": f"""
                     문서들: {docs}
                     출력: """}],
                    )        # GPT-4o 응답 처리
        
                result = completion.choices[0].message.content
                idxs = list(map(int, result.split(', ')))
                selected_docs = [retrieval_results[i] for i in idxs]
                break
            except:
                pass
        
        return selected_docs
        

    
