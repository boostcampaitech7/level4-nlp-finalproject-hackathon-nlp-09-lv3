import pandas as pd
import markdown
from io import StringIO

def markdown_to_df(markdown_text: str) -> pd.DataFrame:
    """
    Convert a markdown table to a pandas DataFrame.
    
    Args:
        markdown_text (str): A string containing the markdown table.
    
    Returns:
        pd.DataFrame: A pandas DataFrame representation of the table.
    """
    # Convert markdown to HTML
    html = markdown.markdown(markdown_text, extensions=['tables'])
    
    # Extract the table using pandas
    dfs = pd.read_html(StringIO(html))
    if dfs:
        return dfs[0]
    else:
        raise ValueError("No table found in the markdown text.")
