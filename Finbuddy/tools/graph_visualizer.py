from crewai.tools import tool
import matplotlib.pyplot as plt

@tool('graph_visualizer')
def graph_visualizer(dataframe):
    """
    Generates a visualization (e.g., bar chart) from a DataFrame.
    """
    # DataFrame을 시각화
    plt.figure(figsize=(10, 6))
    dataframe.plot(kind='bar')
    plt.title("Table Data Visualization")
    plt.xlabel("Categories")
    plt.ylabel("Values")
    plt.savefig("table_visualization.png")
    return "table_visualization.png"