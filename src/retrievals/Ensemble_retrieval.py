from langchain.retrievers import EnsembleRetriever


def ensemble_retrieval(retrievals, topk, weights = [0.5, 0.5], search_type = 'mmr'):
    retriever = EnsembleRetriever(
        retrievers=retrievals,
        weights=weights,
        search_type= search_type,
        k = topk
    )
    return retriever
