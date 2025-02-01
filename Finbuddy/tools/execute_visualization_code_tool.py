import os
import subprocess
import tempfile
import re
from crewai.tools import tool

@tool('execute_visualization_code_tool')
def execute_visualization_code(code_str: str):
    """
    입력받은 파이썬 코드 문자열을 임시 파일에 저장하고 실행하여,
    시각화 이미지를 생성·저장한다.
    
    반환:
        str: 생성된 이미지 파일의 경로 (예: output/images/generated_visualization.png)
    """
    # Markdown 코드 블록에서 코드만 추출 (```python ~ ``` 사이의 내용)
    code_block_match = re.search(r"```(?:python)?\n(.*?)\n```", code_str, re.DOTALL)
    if code_block_match:
        code_str = code_block_match.group(1)
    else:
        # 만약 코드 블록이 발견되지 않으면, 앞뒤의 ```를 제거
        code_str = code_str.strip()
        code_str = re.sub(r"^```(?:python)?\s*\n", "", code_str)
        code_str = re.sub(r"\n```$", "", code_str)

    # 임시 파이썬 파일에 코드 저장
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

    output_path = "output/images/generated_visualization.png"
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"생성된 이미지가 예상 경로에 존재하지 않습니다: {output_path}")
    return output_path
