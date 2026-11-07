from bokeh.plotting import figure, show, output_file
from bokeh.layouts import gridplot

# Load data from files
def load_data(file_path):
    with open(file_path, "r") as file:
        return [float(line.strip()) for line in file]

# File paths
sim1_data = load_data("sim1_data.txt")
sim2_data = load_data("sim2_data.txt")
sim3_data = load_data("sim3_data.txt")

# Line Graphs
line1 = figure(title="Simulation 1: Time to Infect All Cells", x_axis_label="Trial", y_axis_label="Time (seconds)", width=800, height=400)
line1.line(list(range(1, len(sim1_data) + 1)), sim1_data, line_width=2, color="blue", legend_label="Simulation 1")

line2 = figure(title="Simulation 2: Time to Infect All Cells", x_axis_label="Trial", y_axis_label="Time (seconds)", width=800, height=400)
line2.line(list(range(1, len(sim2_data) + 1)), sim2_data, line_width=2, color="green", legend_label="Simulation 2")

line3 = figure(title="Simulation 3: Time to Infect All Cells", x_axis_label="Trial", y_axis_label="Time (seconds)", width=800, height=400)
line3.line(list(range(1, len(sim3_data) + 1)), sim3_data, line_width=2, color="red", legend_label="Simulation 3")

grid = gridplot([
    [line1, line2, line3]
])

# Output to HTML file
output_file("simdataviz.html")
show(grid)