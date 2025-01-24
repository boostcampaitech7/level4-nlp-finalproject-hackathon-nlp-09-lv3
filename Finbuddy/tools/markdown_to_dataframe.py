from crewai.tools import tool
import pandas as pd
import io

@tool('md_to_df')
def markdown_to_dataframe(markdown_table):
    """
    Converts a markdown table into a pandas DataFrame.
    """
    # Markdown 테이블을 DataFrame으로 변환
    table_io = io.StringIO(markdown_table)
    df = pd.read_csv(table_io, sep="|", skipinitialspace=True)
    return df

# def md_to_df(data: Any) -> Any:
#     # Convert markdown to DataFrame
#     if isinstance(data, str):
#         return (
#             pd.read_csv(
#                 StringIO(data),  # Process data
#                 sep="|",
#                 index_col=1,
#             )
#             .dropna(axis=1, how="all")
#             .iloc[1:]
#             .applymap(lambda x: x.strip())
#         )
#     return data