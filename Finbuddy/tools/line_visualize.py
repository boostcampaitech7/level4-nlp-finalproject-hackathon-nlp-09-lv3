from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import matplotlib.pyplot as plt
from typing import List, Type
import os

class LineGraphInput(BaseModel):
    """Input schema for LineGraphTool."""
    x_values: List[float] = Field(..., description="The x-axis values.")
    y_values: List[float] = Field(..., description="The y-axis values.")
    title: str = Field(..., description="The title of the line graph.")
    x_label: str = Field(..., description="Label for the x-axis.")
    y_label: str = Field(..., description="Label for the y-axis.")
    save_path: str = Field("line_graph_output.png", description="Path to save the PNG image.")  # 기본값 설정

class LineGraphTool(BaseTool):
    name: str = "line_graph"
    description: str = "Generates a line graph and saves it as a PNG file."
    args_schema: Type[BaseModel] = LineGraphInput

    def _run(self, x_values: List[float], y_values: List[float], title: str, x_label: str, y_label: str, save_path: str = "line_graph_output.png"):
        """
        Generates a line graph and saves it as a PNG file.

        Args:
            x_values (list): Data points for the x-axis.
            y_values (list): Data points for the y-axis.
            title (str): Title for the graph.
            x_label (str): Label for the x-axis.
            y_label (str): Label for the y-axis.
            save_path (str): Path where the PNG image will be saved (default is 'line_graph_output.png').

        Returns:
            None: Saves the graph as a PNG file and displays it.
        """
        try:
            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.plot(x_values, y_values, marker='o', color='b', linestyle='-', label=title)
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.grid(True)
            plt.legend()
            
            # Save the plot as PNG file
            plt.savefig(save_path, format='png')
            print(f"Graph saved as {save_path}")
            
            # # Display the plot
            # plt.show()
        except Exception as e:
            raise ValueError(f"Failed to generate and save line graph: {str(e)}")


# Example usage
if __name__ == "__main__":
    tool = LineGraphTool()
    # Example data
    x_values = [1, 2, 3, 4, 5]
    y_values = [2, 4, 6, 8, 10]
    title = "Sample Line Graph"
    x_label = "X-axis"
    y_label = "Y-axis"
    
    # Run the tool with default save_path
    tool._run(x_values=x_values, y_values=y_values, title=title, x_label=x_label, y_label=y_label)
