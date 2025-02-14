from modules.Pipeline import pipe_service
from fastapi import FastAPI, Query
from ...schemas import QueryRequest, QueryServiceResponse, Image, ImagesResponse
from glob import glob
from pydantic import BaseModel
import os

pipe = pipe_service(verbose = False)
pipe.setup()
app = FastAPI()

@app.post("/query_closed_domain", response_model=QueryServiceResponse)
async def closed_domain_query(request: QueryRequest):
    answer, file_names, audio_route, chat_count, visualized_name = await pipe.QA(request.query, mode = 'ensemble', search_type = 'closed_domain')
    print('ok')

    return {
        "answer": answer,
        "pdfFileNames" : file_names,
        "audioFileNames" : audio_route,
        'visualized_name' : visualized_name
    }

@app.post("/query_open_domain", response_model = QueryServiceResponse)
async def open_domain_query(request: QueryRequest):
    answer, file_names, audio_route, chat_count, visualized_name = await pipe.QA(request.query, mode = 'ensemble', search_type = 'open_domain')
    return {
        "answer": answer,
        "pdfFileNames" : file_names,
        "audioFileNames" : audio_route,
        'visualized_name' : visualized_name
    }

@app.post("/query", response_model = QueryServiceResponse)
async def service_query(request: QueryRequest):
    answer, file_names, audio_route, chat_count, visualized_name = await pipe.QA(request.query, mode = 'ensemble')
    return {
        "answer": answer,
        "pdfFileNames" : file_names,
        "audioFileNames" : audio_route,
        "visualized_name" : visualized_name
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
    
    # 이미지 파일들이 있는 디렉토리 경로 => 왜 심볼릭 링크로된 경로가 아니라 다이렉트로 되어 있지?
    # file_names = glob('/data/ephemeral/home/level4-nlp-finalproject-hackathon-nlp-09-lv3/src/output/*.png')
    file_names = glob('/data/ephemeral/home/level4-nlp-finalproject-hackathon-nlp-09-lv3/src/front_3/public/static/output/*.png')

    
    for i, file in enumerate(file_names):
        # 파일명에서 확장자 제외한 제목 추출
        title = file.split('/')[-1]
        if title == 'not.png':
            continue
        # 이미지 정보 생성
        image = Image(
            id=i, 
            url='/static/output/' + title,
            title=title
        )
        
        images_list.append(image)
    
    return ImagesResponse(images=images_list)

@app.get("/getImages_folder", response_model=ImagesResponse)
async def get_images_folder(
    folder: str = Query("output", description="이미지 폴더 이름 (static 폴더 내)")
):
    images_list = []
    
    # public 폴더까지 지정합니다.
    base_dir = "/data/level4-nlp-finalproject-hackathon-nlp-09-lv3/src/front_3/public"
    
    # "static" 폴더 내에서 사용자가 전달한 폴더를 참조합니다.
    folder_path = os.path.join(base_dir, "static", folder)
    
    # 폴더 내의 모든 PNG 파일 검색
    file_names = glob(os.path.join(folder_path, "*.png"))
    
    for i, file in enumerate(file_names):
        title = os.path.basename(file)
        if title == 'not.png':
            continue
        
        # base_dir 이후의 상대 경로를 구하면 예: "static/output/카카오_2024_분기별_실적.png"
        relative_path = os.path.relpath(file, base_dir)
        url = "/" + relative_path.replace(os.sep, "/")
        
        image = Image(
            id=i,
            url=url,
            title=title
        )
        images_list.append(image)
    
    return ImagesResponse(images=images_list)


