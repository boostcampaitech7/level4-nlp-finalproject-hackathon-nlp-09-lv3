import http.client
import json
import os
import pandas as pd
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
    
def process_csv_and_generate_embeddings(input_csv_path, output_csv_path):
    """
    CSV 파일의 summary 컬럼에 대해 임베딩을 생성하고 결과를 저장합니다.

    Args:
        input_csv_path (str): 입력 CSV 파일 경로.
        output_csv_path (str): 결과를 저장할 CSV 파일 경로.
    """
    # CSV 파일 읽기
    df = pd.read_csv(input_csv_path)

    # summary 컬럼 확인
    if 'summary' not in df.columns:
        print("Error: 'summary' 컬럼이 CSV 파일에 없습니다.")
        return

    # summary 컬럼의 임베딩 생성
    embeddings = []
    for i, text in enumerate(df['summary']):
        if isinstance(text, str):  # 유효한 문자열인지 확인
            print(f"Processing row {i + 1}/{len(df)}: {text[:30]}...")  # 진행 상황 출력
            embedding = get_text_embedding(text)
            embeddings.append(embedding)
        else:
            embeddings.append(None)  # 비어 있는 값은 None으로 처리

    # 결과를 데이터프레임에 추가
    df['embedding'] = embeddings

    # 결과 저장
    df.to_csv(output_csv_path, index=False)
    print(f"임베딩 생성 완료. 결과가 {output_csv_path}에 저장되었습니다.")

