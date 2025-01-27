from crewai.tools import tool
import pandas as pd
from io import StringIO

@tool("markdown_to_dataframe")
def markdown_to_dataframe(markdown_table: str) -> pd.DataFrame:
    """마크다운 테이블을 pandas DataFrame으로 변환"""
    try:
        lines = markdown_table.strip().split("\n")
        filtered_lines = [line for line in lines if not set(line.strip()).issubset({"|", "-", " "})]
        filtered_table = "\n".join(filtered_lines)
        
        df = pd.read_csv(
            StringIO(filtered_table), 
            sep="|", 
            engine="python", 
            skipinitialspace=True
        )
        
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        df.columns = df.columns.str.strip()
        
        # 숫자 컬럼 변환
        for col in df.columns:
            if col not in ['항목']:
                df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
        
        df.to_csv('dataframe.csv', index=False, encoding='utf-8-sig')
        return df
    except Exception as e:
        raise ValueError(f"DataFrame 변환 오류: {e}")
