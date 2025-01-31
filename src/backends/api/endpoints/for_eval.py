from modules.Pipeline import pipe_eval
from fastapi import FastAPI
from ...schemas import QueryRequest, QueryResponse

pipe = pipe_eval(verbose = False)
pipe.setup(model = 'GPT')
app = FastAPI()

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):

    
    retrieval_results = pipe.Q(request.query, mode = 'ensemble')
    context = [doc.metadata['original_content'] for doc in retrieval_results]

    answer = pipe.A(request.query, retrieval_results)

    return {
        "context": context,
        "answer": answer
    }