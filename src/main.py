


import os
import sys
from uvicorn import run
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # CORS 미들웨어 import

# 프로젝트 루트 경로 설정
project_root = os.getcwd()
sys.path.append(project_root + '/modules')  # modules 디렉터리를 Python 경로에 추가

# FastAPI 라우터 및 앱 불러오기
from backends.api import eval_router, service_router  # eval_router 가져오기

# FastAPI 앱 생성
app = FastAPI()

# CORS 설정 추가
origins = [
    "http://localhost:3001",  # 프론트엔드 도메인 (React 앱)
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인 목록
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

# FastAPI 라우터 등록
app.include_router(eval_router, prefix="/api", tags=["eval"])
app.include_router(service_router, prefix="/api", tags=["service"])

# uvicorn 실행
if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000)