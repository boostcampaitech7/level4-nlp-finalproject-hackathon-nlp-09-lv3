from kiwipiepy import Kiwi
from langchain_community.retrievers import BM25Retriever

class BM25Search:
    def __init__(self, mode = 'kiwi'):
        if mode == 'kiwi':
            # Kiwi 형태소 분석기 설정
            self.kiwi = Kiwi()

    # 형태소 분석을 통해 문서를 토큰화하는 함수
    def kiwi_tokenize(self, text):
        return [token.form for token in self.kiwi.tokenize(text)]
    # bm25 리트리버를 내보냅니다.
    def bm25_retriever(self, documents, topk = 5):
        kiwi_bm25 = BM25Retriever.from_documents(documents, preprocess_func=self.kiwi_tokenize, k = topk)
        return kiwi_bm25
