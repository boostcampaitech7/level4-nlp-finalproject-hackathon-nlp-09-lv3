from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pandas as pd
from io import StringIO
from typing import Type

class MarkdownToDfInput(BaseModel):
    """Input schema for MarkdownToDfTool."""
    markdown: str = Field(..., description="Markdown formatted string to be converted into a DataFrame.")

class MarkdownToDfTool(BaseTool):
    name: str = "markdown_to_df"
    description: str = "Converts a Markdown table to a Pandas DataFrame."
    args_schema: Type[BaseModel] = MarkdownToDfInput

    def _run(self, markdown: str) -> pd.DataFrame:
        """
        Converts a Markdown table into a Pandas DataFrame.

        Args:
            markdown (str): Markdown table as a string.

        Returns:
            pd.DataFrame: DataFrame representation of the Markdown table.
        """
        try:
            # Replace pandas.compat.StringIO with io.StringIO
            df = pd.read_csv(StringIO(markdown), sep="|", engine="python", skipinitialspace=True)
            # Drop empty columns/rows created due to Markdown formatting
            df = df.dropna(how="all", axis=1).dropna(how="all", axis=0)
            df.columns = [col.strip() for col in df.columns]  # Strip whitespace from column names
            df = df.iloc[1:].reset_index(drop=True)  # Skip the alignment row (e.g., `---|---`)
            return df
        except Exception as e:
            raise ValueError(f"Failed to convert Markdown to DataFrame: {str(e)}")

# Example usage
if __name__ == "__main__":
    markdown_table = """
    | Name      | Age | City       |
    |-----------|-----|------------|
    | John Doe  | 28  | New York   |
    | Jane Smith| 34  | Los Angeles|
    | Alice     | 29  | Chicago    |
    """

    tool = MarkdownToDfTool()
    result = tool._run(markdown=markdown_table)
    print(result)
