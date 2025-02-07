from modules.Pipeline import pipe_service
from fastapi import FastAPI
from ...schemas import QueryRequest, QueryServiceResponse

pipe = pipe_service(verbose = False)
pipe.setup()
app = FastAPI()

@app.post("/query_closed_domain", response_model=QueryServiceResponse)
async def closed_domain_query(request: QueryRequest):
    answer, file_names, audio_route, chat_count = await pipe.QA(request.query, mode = 'ensemble', search_type = 'closed_domain')
    print('ok')

    return {
        "answer": answer,
        "pdfFileNames" : file_names,
        "audioFileNames" : audio_route,
    }

@app.post("/query_open_domain", response_model = QueryServiceResponse)
async def open_domain_query(request: QueryRequest):
    answer, file_names, audio_route, chat_count = await pipe.QA(request.query, mode = 'ensemble', search_type = 'open_domain')
    return {
        "answer": answer,
        "pdfFileNames" : file_names,
        "audioFileNames" : audio_route,
    }

@app.post("/query", response_model = QueryServiceResponse)
async def service_query(request: QueryRequest):
    answer, file_names, audio_route, chat_count = await pipe.QA(request.query, mode = 'ensemble')
    return {
        "answer": answer,
        "pdfFileNames" : file_names,
        "audioFileNames" : audio_route,
    }

@app.get("/reset_output")
async def reset_output():
    pipe.reset_output()
    return {
        "answer": "Output reset successfully"
    }