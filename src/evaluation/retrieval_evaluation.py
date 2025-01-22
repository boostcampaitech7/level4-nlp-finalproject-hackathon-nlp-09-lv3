from DB.chromadb_storing import ChromaDB
from langchain.schema import Document
from utils import get_only_paragraphs, get_all_datas, create_documents
from retrievals import bm25, dpr, ensemble
from evaluation import retrieval_evaluate
import pandas as pd
import time

BASE_DIR = '../datas' # 데이터가 저장돼 있는 루트
df = get_only_paragraphs(BASE_DIR)

# 데이터프레임의 행들을 각각 Document타입으로 바꾼 뒤, 리스트에 담습니다.
documents = create_documents(df)

# add_docs를 통해 문서들을 저장합니다.
collection_name = 'chrdb.db'
DB = ChromaDB(collection_name)
DB.add_docs(documents)
# verify_db를 통해 db내의 데이터 수를 확인할 수 있고, db객체를 받을 수 있습니다.
db = DB.verify_db()
# 데이터 저장
DB.save_collection()
# 데이터 로드
DB.load_collection()

topk = 50

DPRRetriever = dpr(db, topk = topk)
BM25Retriever = bm25(documents, topk =topk)

retrievals = [DPRRetriever, BM25Retriever]
weights = [0.5, 0.5]
search_type = 'mmr'
ensemble_retriever = ensemble(retrievals, topk = topk, weights = weights, search_type = search_type)

def retrieval_evaluate(retrieval, eval_dataset, k):
    total = len(eval_dataset)
    answer = 0
    for i, row in eval_dataset.iterrows():
        question = row['question']
        context = row['context']

        # 앙상블의 경우 그냥 topK로 해버리면 작동이 잘 되지 않아 후처리 필요
        if retrieval == 'ensemble_retriever':
            results = retrieval.invoke(question)
            sorted_results = sorted(results, key=lambda x: x.metadata.get('score', 0), reverse=True)
            retrieval_results = sorted_results[:k]

        else: 
            retrieval_results = retrieval.invoke(question)
        docs = [doc.metadata['original_content'] for doc in retrieval_results]
        if context in docs:
            answer += 1
    print('acc:', round(answer / total, 4))

eval_dataset = pd.read_csv('../processed_data/qa_validation_dataset_4_cleaning.csv')

start_time = time.time()
# retrieval과 evaldataset을 통해 acc를 평가
retrieval_evaluate(retrieval=BM25Retriever, eval_dataset = eval_dataset, k=50)
end_time = time.time()
print(f"{end_time - start_time:.6f} seconds")
