from crewai.tools import tool
import matplotlib.pyplot as plt

@tool('bar_visualize')
def bar_visualize(data, labels, title="Bar Chart", xlabel="Categories", ylabel="Values"):
    """
    Generate a bar chart visualization.
    
    Args:
        data (list): List of values for the bar chart.
        labels (list): List of labels corresponding to the data.
        title (str): Title of the bar chart.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
    
    Returns:
        None: Saves the bar chart as an image file.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(labels, data, color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("../../bar_chart.png")
    plt.close()
