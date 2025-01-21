def retrieval_evaluate(retrieval, eval_dataset):
    total = len(eval_dataset)
    answer = 0
    for i, row in eval_dataset.iterrows():
        question = row['question']
        context = row['context']
        retrieval_results = retrieval.invoke(question)
        docs = [doc.metadata['original_content'] for doc in retrieval_results]
        if context in docs:
            answer += 1
    print('acc:', round(answer / total, 4))