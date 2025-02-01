import os
from crewai.tools import tool
from src.modules.Pipeline import pipe_eval

@tool('generate_visualization_code_tool')
def generate_visualization_code(query: str, table_str: str):
    """
    초기 쿼리와 markdown 형식의 테이블 데이터를 받아, 
    matplotlib를 사용하여 해당 데이터를 시각화하고 이미지로 저장하는 파이썬 코드를 생성한다.
    
    LLM을 통해 코드를 생성하며, 만약 오류가 발생하면 2~3번 보정한다.
    
    Returns:
        str: 생성된 파이썬 코드 문자열
    """
    prompt = f"""
    아래의 초기 쿼리와 테이블 데이터를 참고하여, 파이썬의 matplotlib를 사용해서 
    테이블 데이터를 시각화하는 코드를 작성해줘. 
    시각화된 이미지는 "output/images/generated_visualization.png" 경로에 저장되어야 해.
    또한, 코드 내에서 발생할 수 있는 오류를 자동으로 보정하는 로직(예: try-except)을 2~3번 반복 보정하도록 포함해줘.

    초기 쿼리: {query}

    테이블 데이터:
    {table_str}

    함수 이름은 visualize_table_generated 로 작성해주고, 
    함수 호출 시에 바로 실행될 수 있도록 __main__ 부분도 포함해줘.
    """
    
    # LLM 파이프라인 세팅 (pipe_eval은 retrieval tool과 동일하게 활용)
    pipe = pipe_eval(verbose=True)
    pipe.setup(model='GPT')
    generated_code = None
    
    # 2~3회 반복하여 코드 보정 시도
    for attempt in range(3):
        generated_code = pipe.Q(prompt, mode='code_generation')
        # 간단한 검증: 함수 정의와 plt.savefig 코드가 포함되어 있는지 확인
        if "def visualize_table_generated" in generated_code and "plt.savefig" in generated_code:
            break
        # 보정을 위한 힌트를 추가하여 prompt 업데이트
        prompt += "\n# 이전 코드에서 오류를 발견했으니, 이를 보정하여 다시 작성해줘."
    
    return generated_code
