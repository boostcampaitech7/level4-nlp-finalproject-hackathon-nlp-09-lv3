from crewai.tools import tool

@tool('table_analyzer')
def table_analyzer(table_data):
    """
    Analyzes the given table data and returns a summary.
    """
    # 테이블 데이터를 분석하여 주요 정보를 요약
    summary = f"The table contains {len(table_data.splitlines())} rows and X columns."
    return summary
