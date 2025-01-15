import http.client
import json
import os
from dotenv import load_dotenv
load_dotenv()
def get_text_embedding(text):
    """
    HyperClova API를 사용하여 텍스트 임베딩을 생성합니다.

    Args:
        text (str): 입력 텍스트.

    Returns:
        list: 텍스트 임베딩 벡터. 오류 발생 시 'Error' 문자열 반환.
    """
    # 환경 변수에서 API 키 가져오기
    host = 'clovastudio.apigw.ntruss.com'
    api_key = os.environ['NAVERCLOUD_EMBEDDING_KEY']
    api_key_primary_val = os.environ['NAVERCLOUD_EMBEDDING_PRIMARY_KEY']
    request_id = '8c4abff05a38493aac0cb39a43adf8be'

    # 요청 데이터 생성
    completion_request = {
        "text": text
    }

    # HTTP 헤더 설정
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'X-NCP-CLOVASTUDIO-API-KEY': api_key,
        'X-NCP-APIGW-API-KEY': api_key_primary_val,
        'X-NCP-CLOVASTUDIO-REQUEST-ID': request_id
    }

    try:
        # HTTPS 연결 및 요청
        conn = http.client.HTTPSConnection(host)
        conn.request('POST', '/serviceapp/v1/api-tools/embedding/v2/ffd12341df5941aa88630ca1b9656a7a', 
                     json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()

        # 결과 반환
        if result['status']['code'] == '20000':
            return result['result']['embedding']
        else:
            return 'Error: ' + result.get('status', {}).get('message', 'Unknown error occurred.')

    except Exception as e:
        return f"Error: {str(e)}"
