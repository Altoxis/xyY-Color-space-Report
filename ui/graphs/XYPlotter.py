import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from concurrent.futures import ThreadPoolExecutor
import config
from core.color_functions import xyY_to_XYZ, XYZ_to_sRGB, find_closest_colors  # Import find_closest_colors
from ui.graphs.EllipsePlotter import EllipsePlotter  # Import EllipsePlotter

class XYPlotter(QWidget):
    data_ready = QtCore.pyqtSignal(object, object, object)

    def __init__(self, parent=None):
        super(XYPlotter, self).__init__(parent)
        self.initUI()
        self.scatter = None
        self.center_point = None  # To track the center point
        self.sample_points = []  # To track sample points
        self.sample_labels = []  # To track sample labels
        self.ellipse_plotter = EllipsePlotter(self.plot_widget)  # Initialize EllipsePlotter
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.data_ready.connect(self.update_plot)
        self.start_calculation()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1F1F1F')  # Set background to dark grey
        self.layout.addWidget(self.plot_widget)
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.setMinimumHeight(400)
        self.setLayout(self.layout)

    def calculate_color_data(self, x_center, y_center, Y):
        step = 0.0005  # Adjust step size for better performance
        x_values = np.arange(x_center - 0.015, x_center + 0.015 + step, step)
        y_values = np.arange(y_center - 0.015, y_center + 0.015 + step, step)

        x_grid, y_grid = np.meshgrid(x_values, y_values)
        x_flat = x_grid.flatten()
        y_flat = y_grid.flatten()

        X, Y_value, Z = xyY_to_XYZ(x_flat, y_flat, Y)
        R, G, B = XYZ_to_sRGB(X, Y_value, Z)

        data = np.vstack((x_flat, y_flat, R, G, B)).T
        return data

    def start_calculation(self):
        try:
            x_center, y_center, Y = config.xyY_values
        except ValueError:
            self.label.setText("Invalid values in config.py. Please provide three valid numbers.")
            return

        if not (0 <= Y <= 1) or not (0 <= x_center <= 1) or not (0 <= y_center <= 1):
            self.label.setText("Values in config.py must be between 0 and 1.")
            return

        future = self.executor.submit(self.calculate_color_data, x_center, y_center, Y)
        future.add_done_callback(self.handle_data_result)

    def handle_data_result(self, future):
        try:
            data = future.result()
        except Exception as e:
            self.label.setText(f"Error: {e}")
            return

        if data.size == 0:
            self.label.setText("No data found.")
            return

        x_plot = data[:, 0]
        y_plot = data[:, 1]
        colors = np.array([pg.mkColor((int(r), int(g), int(b))) for r, g, b in data[:, 2:5]])

        self.data_ready.emit(x_plot, y_plot, colors)

    @QtCore.pyqtSlot(object, object, object)
    def update_plot(self, x_plot, y_plot, colors):
        if self.scatter:
            self.scatter.setData(x=x_plot, y=y_plot, brush=colors, size=0.0005, symbol='s', pen=None, pxMode=False)
        else:
            self.scatter = pg.ScatterPlotItem(x=x_plot, y=y_plot, brush=colors, size=0.0005, symbol='s', pen=None, pxMode=False)
            self.plot_widget.addItem(self.scatter)

        # Remove the old center point if it exists
        if self.center_point:
            self.plot_widget.removeItem(self.center_point)

        # Add the small square at the position specified in config
        x_center, y_center, _ = config.xyY_values
        spot_size = 0.01  # Size of the spot

        # Create a black square with a white border for the new center point
        self.center_point = pg.ScatterPlotItem([x_center], [y_center], size=spot_size / 20, pen=pg.mkPen('w'), brush=pg.mkBrush('k'), pxMode=False)
        self.plot_widget.addItem(self.center_point)

        # Plot sample points from config.Samples
        self.plot_sample_points()

        # Enable antialiasing for better visual quality
        self.plot_widget.setAntialiasing(True)

    def plot_sample_points(self):
        # Clear previously plotted sample points and labels
        for sample_point in self.sample_points:
            self.plot_widget.removeItem(sample_point)
        for sample_label in self.sample_labels:
            self.plot_widget.removeItem(sample_label)
        self.sample_points.clear()
        self.sample_labels.clear()

        # Plot new sample points and labels
        for sample in config.Samples:
            name = sample["name"]
            x = float(sample["x"])
            y = float(sample["y"])
            Y = float(sample["Y"])
            X, Y_value, Z = xyY_to_XYZ(x, y, Y)
            R, G, B = XYZ_to_sRGB(X, Y_value, Z)

            color = pg.mkColor((int(R), int(G), int(B)))
            sample_point = pg.ScatterPlotItem([x], [y], size=0.001, pen=pg.mkPen('k'), brush=pg.mkBrush(color), pxMode=False)
            self.plot_widget.addItem(sample_point)
            self.sample_points.append(sample_point)

            # Add the sample name as a text label
            sample_label = pg.TextItem(name, anchor=(0, 1), color='w')
            sample_label.setPos(x, y)
            self.plot_widget.addItem(sample_label)
            self.sample_labels.append(sample_label)

        # Re-plot ellipses around the plotted color to update lines and labels
        self.plot_ellipses()

    def plot_ellipses(self):
        # Get the main plotted color from config.xyY_values
        x_center, y_center, Y_center = config.xyY_values

        # Plot ellipses around the plotted color
        self.ellipse_plotter.plot_selected_color("Plotted Color", x_center, y_center, Y_center)
