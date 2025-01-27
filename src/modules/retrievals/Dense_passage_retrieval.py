def DPRRetriever(db, topk = 5):
    return db.as_retriever(search_kwargs={"k": topk,})