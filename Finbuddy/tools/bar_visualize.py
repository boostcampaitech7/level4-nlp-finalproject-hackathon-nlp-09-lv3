from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pandas as pd
import matplotlib.pyplot as plt
from typing import Type, Optional

class BarGraphInput(BaseModel):
    """Input schema for BarGraphTool."""
    data: dict = Field(..., description="Dictionary containing the data for the bar graph (e.g., {'Category': [values], 'Values': [values]}).")
    x_label: str = Field(..., description="Label for the x-axis (column name in the dictionary).")
    y_label: str = Field(..., description="Label for the y-axis (column name in the dictionary).")
    title: Optional[str] = Field(None, description="Title of the bar graph.")
    output_file: Optional[str] = Field("bar_graph_output.png", description="Optional output file path to save the graph.")

class BarGraphTool(BaseTool):
    name: str = "bar_graph_tool"
    description: str = "Creates a bar graph from input data."
    args_schema: Type[BaseModel] = BarGraphInput

    def _run(self, data: dict, x_label: str, y_label: str, title: Optional[str] = None, output_file: Optional[str] = None) -> str:
        """
        Creates a bar graph from the given data.

        Args:
            data (dict): Dictionary with data for the bar graph.
            x_label (str): Column name for the x-axis.
            y_label (str): Column name for the y-axis.
            title (str, optional): Title of the graph. Defaults to None.
            output_file (str, optional): Path to save the graph. Defaults to None.

        Returns:
            str: Success message or path to the saved graph.
        """
        try:
            # Convert dictionary to DataFrame
            df = pd.DataFrame(data)

            # Plot the bar graph
            plt.figure(figsize=(10, 6))
            plt.bar(df[x_label], df[y_label], color="skyblue", edgecolor="black")
            plt.xlabel(x_label, fontsize=12)
            plt.ylabel(y_label, fontsize=12)
            if title:
                plt.title(title, fontsize=14)
            plt.xticks(rotation=45)
            plt.tight_layout()

            # Save or show the graph
            if output_file:
                plt.savefig(output_file)
                plt.close()
                return f"Bar graph saved to {output_file}"
            else:
                plt.show()
                return "Bar graph displayed successfully."
        except Exception as e:
            raise ValueError(f"Failed to create bar graph: {str(e)}")

# Example usage
if __name__ == "__main__":
    data = {
        "Category": ["A", "B", "C", "D"],
        "Values": [10, 15, 7, 12]
    }
    tool = BarGraphTool()
    result = tool._run(data=data, x_label="Category", y_label="Values", title="Sample Bar Graph", output_file="bar_graph.png")
    print(result)
