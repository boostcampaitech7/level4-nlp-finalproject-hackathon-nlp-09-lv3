import matplotlib.pyplot as plt

def line_visualize(data, labels, title="Line Chart", xlabel="X-Axis", ylabel="Y-Axis"):
    """
    Generate a line chart visualization.
    
    Args:
        data (list): List of values for the line chart.
        labels (list): List of x-axis labels corresponding to the data.
        title (str): Title of the line chart.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
    
    Returns:
        None: Saves the line chart as an image file.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(labels, data, marker='o', color='blue', linestyle='-')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("line_chart.png")
    plt.close()
