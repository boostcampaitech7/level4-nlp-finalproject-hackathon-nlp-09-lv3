import pandas as pd
import requests
from glob import glob
import pdfplumber
import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
load_dotenv()



def image_summarization(image_path, investment, company):
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)
    # Open the image file and encode it as a base64 string
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system", 
                "content": 

                "당신은 RAG 시스템을 위한 요약가입니다. RAG 시스템을 위해 검색 엔진이 연관 문서를 잘 검색할 수 있도록 이미지를 설명해야 합니다."

                },
                {"role": "user", "content": [{"type": "text", "text": 
                                            
                f"""
                다음은 {investment}의 {company}에 대한 리포트 중 일부입니다.
                이미지가 무엇을 나타내고 있는지 Retrieval을 위한 설명을 200자 이내로 작성하세요.
                설명에 회사 이름을 반드시 포함하세요.
                만약 이미지가 사람밀 경우, [사람 이미지] 라고 출력하세요.
                [출력 형식]
                설명 : [그래프에 대한 설명]
                """

                },
                {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )

    result = response.choices[0].message.content
    return result



def table_summarization(image_path, investment, company):
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)
    # Open the image file and encode it as a base64 string
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system", 
                "content": 

                "당신은 RAG 시스템을 위한 요약가입니다. RAG 시스템을 위해 검색 엔진이 연관 문서를 잘 검색할 수 있도록 테이블을 설명해야 합니다."

                },
                {"role": "user", "content": [{"type": "text", "text": 
                                            
                f"""
                다음은 {investment}의 {company}에 대한 리포트 중 일부입니다.
                주어진 테이블을 마크다운으로 표현하세요.
                테이블이 무엇을 나타내고 있는지 Retrieval을 위한 테이블에 대한 설명을 200자 이내로 작성하세요.
                요약에 회사 이름을 반드시 포함하세요.

                [출력 형식]
                [마크다운으로 표현된 Table]
                
                설명 : [테이블에 대한 설명]
                
                '''markdown'''과 같은 표현은 삽입하지 마세요.
                """
                
                },
                {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )

    result = response.choices[0].message.content

    return result

def text_summarization(html_content, investment, company):
    api_key = os.environ['OPENAI_API_KEY']
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system", 
                "content": "당신은 RAG 시스템을 위한 요약가입니다. RAG 시스템을 위해 검색 엔진이 연관 문서를 잘 검색할 수 있도록 text를 요약해야 합니다."
            },
            {
                "role": "user", 
                "content": f"""
                다음은 {investment}의 {company}에 대한 리포트 중 일부입니다.
                주어진 글에 대해 Retrieval을 위한 요약을 200자 이내로 작성하세요.
                요약에 회사 이름을 반드시 포함하세요.

                [원문]
                {html_content}

                [출력 형식]
                
                요약 : [글에 대한 요약]
                """
            }
        ],
        temperature=0.0,
    )

    summary = response.choices[0].message.content
    return summary


def text_summarization_Hyperclova(html_content, investment, company):
    # Hyperclova API 요청 설정
    host = 'https://clovastudio.stream.ntruss.com'
    api_key = os.environ['HyperclovaX_API_KEY']
    api_key_primary_val = os.environ['HyperclovaX_PRIVATE_KEY']
    request_id = '95b33ce0c69540c184f917a08529e8b5'

    headers = {
        'X-NCP-CLOVASTUDIO-API-KEY': api_key,
        'X-NCP-APIGW-API-KEY': api_key_primary_val,
        'X-NCP-CLOVASTUDIO-REQUEST-ID': request_id,
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'  # JSON 형식으로 응답받기
    }

    # 요청 데이터 구성
    preset_text = [
        {
            "role": "system", 
            "content": "당신은 RAG 시스템을 위한 요약가입니다. RAG 시스템을 위해 검색 엔진이 연관 문서를 잘 검색할 수 있도록 text를 요약해야 합니다."
        },
        {
                "role": "user", 
                "content": f"""
                다음은 {investment}의 {company}에 대한 리포트 중 일부입니다.
                주어진 글에 대해 Retrieval을 위한 요약을 200자 이내로 작성하세요.
                요약에 회사 이름을 반드시 포함하세요.

                [원문]
                {html_content}

                [출력 형식]
                
                요약 : [글에 대한 요약]
                """
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
        f"{host}/serviceapp/v1/chat-completions/HCX-003",
        headers=headers,
        json=request_data,
        stream=False  # 스트리밍 비활성화
    )

    # 요청 성공 여부 확인
    response.raise_for_status()

    # 결과 반환
    result = response.json()
    return result['result']['message']['content']
