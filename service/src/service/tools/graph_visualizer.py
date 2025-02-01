# from crewai.tools import tool
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# @tool("create_visualization")
# def create_visualization(csv_path: str) -> str:
#     """재무 데이터 시각화 도구"""
#     try:
#         df = pd.read_csv(csv_path)
        
#         # 스타일 설정
#         plt.style.use('dark_background')
#         plt.figure(figsize=(15, 10))
        
#         # 연도별 주요 지표 시각화
#         for metric in ['매출액 (십억원)', '영업이익 (십억원)', '순이익 (십억원)']:
#             plt.plot(df.columns[1:], df[df['항목'] == metric].iloc[:, 1:].values[0], 
#                     marker='o', label=metric)
        
#         plt.title('주요 재무지표 추이', fontsize=15, pad=20)
#         plt.legend(fontsize=12)
#         plt.grid(True, alpha=0.3)
        
#         # 저장 및 반환
#         plt.savefig('report.png', dpi=300, bbox_inches='tight')
#         plt.close()
        
#         return "report.png가 생성되었습니다."
#     except Exception as e:
#         raise ValueError(f"시각화 생성 오류: {e}")

# src/tools/graph_visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from crewai.tools import tool

@tool("create_visualization")
def create_visualization(csv_path: str) -> str:
    """
    주어진 CSV 파일을 불러와 간단한 라인 그래프 등을 그려 report.png 로 저장.
    """
    try:
        df = pd.read_csv(csv_path)

        plt.style.use('dark_background')
        plt.figure(figsize=(12, 8))

        # 예시로 항목이 '매출액 (십억원)', '영업이익 (십억원)', '순이익 (십억원)' 등일 경우
        metrics = ['매출액 (십억원)', '영업이익 (십억원)', '순이익 (십억원)']
        # 첫 번째 컬럼이 "항목", 나머지는 연도별 수치라고 가정
        if '항목' not in df.columns:
            raise ValueError("CSV에 '항목' 컬럼이 없으므로 예시 그래프 작성 불가")

        # 항목별 라인 그래프
        for metric in metrics:
            if metric in df['항목'].values:
                row_data = df[df['항목'] == metric].iloc[:, 1:].values[0]  # 연도별 값
                col_labels = df.columns[1:]  # 실제로는 연도 (2022, 2023, 2024F 등)
                plt.plot(col_labels, row_data, marker='o', label=metric)

        plt.title('주요 재무지표 추이', fontsize=16, pad=20)
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)

        plt.savefig('report.png', dpi=300, bbox_inches='tight')
        plt.close()

        return "report.png가 생성되었습니다."
    except Exception as e:
        raise ValueError(f"시각화 생성 오류: {e}")

