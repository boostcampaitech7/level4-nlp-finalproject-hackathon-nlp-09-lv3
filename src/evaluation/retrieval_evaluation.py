import time
from tqdm import tqdm

def check_acc(retrieval, eval_dataset, k):
    total = len(eval_dataset)
    answer = 0
    for _, row in tqdm(eval_dataset.iterrows()):
        question = row['question']
        context = row['context']

        # 앙상블의 경우 그냥 topK로 해버리면 작동이 잘 되지 않아 후처리 필요
        if retrieval == 'ensemble_retriever':
            k = k*2
            results = retrieval.invoke(question)
            sorted_results = sorted(results, key=lambda x: x.metadata.get('score', 0), reverse=True)
            retrieval_results = sorted_results[:k]

        else: 
            retrieval_results = retrieval.invoke(question)
        docs = [doc.metadata['original_content'] for doc in retrieval_results]
        if context in docs:
            answer += 1
    acc = round(answer / total, 4)
    return acc

def retrieval_evaluate(retrieval, eval_dataset, k=5):
    start_time = time.time()
    acc = check_acc(retrieval, eval_dataset, k=5)
    end_time = time.time()
    print('acc:', acc)
    print(f"{end_time - start_time:.6f} seconds")
