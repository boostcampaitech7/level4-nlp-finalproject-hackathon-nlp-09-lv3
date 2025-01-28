import os
import sys
from uvicorn import run  # uvicorn import

# 프로젝트 루트 경로 설정
project_root = os.getcwd()
sys.path.append(project_root + '/modules')  # modules 디렉터리를 Python 경로에 추가

# FastAPI 라우터 및 앱 불러오기
from backends.api import eval_router  # eval_router 가져오기
from fastapi import FastAPI

# FastAPI 앱 생성 및 라우터 등록
app = FastAPI()
app.include_router(eval_router, prefix="/api", tags=["eval"])

# uvicorn 실행
if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)
