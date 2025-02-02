import os
import subprocess
import tempfile
import re
from crewai.tools import tool

@tool('execute_visualization_code_tool')
def execute_code(code_str: str, ):
    """
    입력받은 파이썬 코드 문자열을 임시 파일에 저장하고 실행하여,
    시각화 이미지를 생성·저장한다.
    input의 ['code'] 부분만을 활용하여 완전한 형태의 코드를 넣어야 한다.
    [경로]
    str: 생성된 이미지 파일의 경로 (예: output/image_name.png)
    """
    
    with open('test.txt', 'w', encoding = 'utf-8') as f:
        f.write(code_str)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
        tmp_file.write(code_str)
        tmp_filename = tmp_file.name

    # 저장된 파일 실행
    try:
        result = subprocess.run(
            ['python', tmp_filename],
            capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"코드 실행 중 오류 발생:\nSTDERR: {e.stderr}\nSTDOUT: {e.stdout}")
    finally:
        # 임시 파일 삭제 (삭제하지 않으려면 주석 처리)
        os.remove(tmp_filename)