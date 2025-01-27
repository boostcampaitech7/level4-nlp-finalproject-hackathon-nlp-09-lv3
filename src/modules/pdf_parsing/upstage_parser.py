import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

def parsing(BASE_DIR, route):
    # 디렉터리 이름 및 파일 이름 설정
    dir_name = os.path.join(BASE_DIR, route.split('/')[-1][:-4])
    file_name = route.split('/')[-1][:-4] + '.json'
    file_path = os.path.join(dir_name, file_name)
    api_key = os.environ['UPSTAGE_API_KEY']

    # 디렉터리 없으면 생성
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # 파일 존재 여부 확인
    if os.path.exists(file_path):
        print(f"{file_name} 파일이 이미 존재합니다. 기존 파일을 불러옵니다.")
        with open(file_path, 'r', encoding='utf-8') as f:
            result = json.load(f)
        return result  # 기존 파일 내용 반환

    # API 엔드포인트
    url = "https://api.upstage.ai/v1/document-ai/document-parse"
    input_file_path = route

    # HTTP 요청 헤더 및 파일 설정
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    files = {
        "document": open(input_file_path, "rb")  # 파일을 바이너리로 읽어 업로드
    }

    # POST 요청 전송
    response = requests.post(url, headers=headers, files=files)

    # 결과 확인
    if response.status_code == 200:
        print(f"{input_file_path.split('/')[-1]} 파싱 성공!")
    else:
        print(f"{input_file_path.split('/')[-1]} 파싱 중 오류 발생: {response.status_code}")
        return None

    # JSON 응답 저장
    result = response.json()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    return result  # 새로 요청한 결과 반환
