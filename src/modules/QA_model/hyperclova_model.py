from QA_model.base_model import BaseModel
import os
from dotenv import load_dotenv
import requests
load_dotenv()
class HyperClovaModel(BaseModel):
    def __init__(self):
    # Hyperclova API 요청 설정
        self.host = 'https://clovastudio.stream.ntruss.com'
        api_key = os.environ['HyperclovaX_API_KEY']
        api_key_primary_val = os.environ['HyperclovaX_PRIVATE_KEY']
        request_id = '95b33ce0c69540c184f917a08529e8b5'

        self.headers = {
            'X-NCP-CLOVASTUDIO-API-KEY': api_key,
            'X-NCP-APIGW-API-KEY': api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': request_id,
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json'  # JSON 형식으로 응답받기
        }
    def answering(self, prompt):
        # 요청 데이터 구성
        preset_text = [
            {
                "role": "system", 
                "content": "당신은 참고문서들을 활용하여 질문에 대한 답변을 제공하는 주식 전문가입니다."
            },
            {
                    "role": "user", 
                    "content": prompt
            }
        ]

        request_data = {
            'messages': preset_text,
            'topP': 0.8,
            'topK': 0,
            'maxTokens': 256,
            'temperature': 0.5,
            'repeatPenalty': 5.0,
            'stopBefore': [],
            'includeAiFilters': True,
            'seed': 0
        }

        # API 요청
        response = requests.post(
            f"{self.host}/serviceapp/v1/chat-completions/HCX-003",
            headers=self.headers,
            json=request_data,
            stream=False  # 스트리밍 비활성화
        )

        # 요청 성공 여부 확인
        response.raise_for_status()

        # 결과 반환
        result = response.json()
        return result['result']['message']['content']