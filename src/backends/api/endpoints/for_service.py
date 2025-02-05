from modules.Pipeline import pipe_service
from fastapi import FastAPI
from ...schemas import QueryRequest, QueryServiceResponse

pipe = pipe_service(verbose = False)
pipe.setup()
app = FastAPI()

@app.post("/query_closed_domain", response_model=QueryServiceResponse)
async def query(request: QueryRequest):
    answer = pipe.QA(request.query, mode = 'ensemble', search_type = 'closed_domain')

    return {
        "answer": answer
    }

@app.post("/query_open_domain", response_model = QueryServiceResponse)
async def query(request: QueryRequest):
    answer = pipe.QA(request.query, mode = 'ensemble', search_type = 'open_domain')
    return {
        "answer": answer
    }

@app.post("/query", response_model = QueryServiceResponse)
async def query(request: QueryRequest):
    answer = pipe.QA(request.query, mode = 'ensemble')
    return {
        "answer" : answer
    }

@app.get("/reset_output")
async def reset_output():
    pipe.reset_output()
    return {
        "answer": "Output reset successfully"
    }