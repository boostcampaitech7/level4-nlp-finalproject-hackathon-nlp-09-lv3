from modules.Pipeline import pipe_service
from fastapi import FastAPI
from ...schemas import QueryRequest, QueryServiceResponse, Image, ImagesResponse
from glob import glob
from pydantic import BaseModel
import os

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
@app.get("/getImages", response_model=ImagesResponse)
async def get_images():
    images_list = []
    
    # 이미지 파일들이 있는 디렉토리 경로
    file_names = glob('/data/ephemeral/home/level4-nlp-finalproject-hackathon-nlp-09-lv3/src/output/*.png')
    
    for i, file in enumerate(file_names):
        # 파일명에서 확장자 제외한 제목 추출
        title = file.split('/')[-1]
        
        # 이미지 정보 생성
        image = Image(
            id=i, 
            url='/static/output/' + title,
            title=title
        )
        
        images_list.append(image)
    
    return ImagesResponse(images=images_list)