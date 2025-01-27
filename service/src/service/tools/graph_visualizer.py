from crewai.tools import tool
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@tool("create_visualization")
def create_visualization(csv_path: str) -> str:
    """재무 데이터 시각화 도구"""
    try:
        df = pd.read_csv(csv_path)
        
        # 스타일 설정
        plt.style.use('dark_background')
        plt.figure(figsize=(15, 10))
        
        # 연도별 주요 지표 시각화
        for metric in ['매출액 (십억원)', '영업이익 (십억원)', '순이익 (십억원)']:
            plt.plot(df.columns[1:], df[df['항목'] == metric].iloc[:, 1:].values[0], 
                    marker='o', label=metric)
        
        plt.title('주요 재무지표 추이', fontsize=15, pad=20)
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # 저장 및 반환
        plt.savefig('report.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return "report.png가 생성되었습니다."
    except Exception as e:
        raise ValueError(f"시각화 생성 오류: {e}")
