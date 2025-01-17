from typing import List
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from rank_bm25 import BM25Okapi
from kiwipiepy import Kiwi


class BM25Search(BaseRetriever):
    def __init__(self, documents: List[Document], k: int = 5, mode = 'kiwi'):
        self.documents = documents
        self.k = k
        if mode == 'kiwi':
            kiwi = Kiwi()
            self.tokenize_fn = kiwi.tokenize
        self.bm25 = self.__initialize_bm25()

    def _initialize_bm25(self):
        # 토큰화된 문서 리스트를 BM25에 입력

        tokenized_corpus = [[token.form for token in self.tokenize_fn(doc.page_content.lower())]for doc in self.documents]

        return BM25Okapi(tokenized_corpus)
    
    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None
    ) -> List[Document]:
        # 쿼리 토큰화
        tokenized_query = [token.form for token in self.tokenize_fn(query.lower())]
        
        # BM25 점수 계산
        scores = self.bm25.get_scores(tokenized_query)
        
        # 가장 높은 k개의 문서 선택
        top_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )[:self.k]
        
        matching_documents = [self.documents[i] for i in top_indices]
        return matching_documents