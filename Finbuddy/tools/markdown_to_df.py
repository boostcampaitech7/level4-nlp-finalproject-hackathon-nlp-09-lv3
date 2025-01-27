import pandas as pd
from crewai.tools import tool
from io import StringIO

@tool('markdown_to_df')
def markdown_to_df(markdown: str) -> pd.DataFrame:
    """Markdown 테이블을 DataFrame으로 변환하는 도구."""
    # Markdown을 문자열로 받은 후, StringIO로 처리하여 pandas의 read_csv로 DataFrame으로 변환
    markdown = markdown.replace('|', ',')  # '|'를 ','로 바꿔서 csv 형식으로 만듬
    markdown_io = StringIO(markdown)
    df = pd.read_csv(markdown_io, sep=",", engine="python")
    return df


# from crewai.tools import tool
# import pandas as pd
# import markdown
# from io import StringIO

# @tool('markdown_to_df')
# def markdown_to_df(markdown_text: str) -> pd.DataFrame:
#     """
#     Convert a markdown table to a pandas DataFrame.
    
#     Args:
#         markdown_text (str): A string containing the markdown table.
    
#     Returns:
#         pd.DataFrame: A pandas DataFrame representation of the table.
#     """
#     # Convert markdown to HTML
#     html = markdown.markdown(markdown_text, extensions=['tables'])
    
#     # Extract the table using pandas
#     dfs = pd.read_html(StringIO(html))
#     if dfs:
#         return dfs[0]
#     else:
#         raise ValueError("No table found in the markdown text.")

# from crewai.tools import tool
# import pandas as pd
# from io import StringIO

# @tool('markdown_to_df')
# def markdown_to_df(markdown_data: str):
#     """Convert markdown formatted table data into a pandas DataFrame."""
    
#     # 마크다운을 CSV로 처리하여 pandas DataFrame 생성
#     df = pd.read_csv(StringIO(markdown_data), delimiter="|", skipinitialspace=True)

#     # 불필요한 첫 번째 열과 마지막 열을 제거
#     df = df.drop(df.columns[[0, -1]], axis=1)

#     # 컬럼 이름을 정리
#     df.columns = [col.strip() for col in df.columns]

#     # 결과 DataFrame 반환
#     return df


