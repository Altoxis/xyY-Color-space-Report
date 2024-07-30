import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from pyqtgraph import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from concurrent.futures import ThreadPoolExecutor
import config
from core.color_functions import xyY_to_XYZ, XYZ_to_sRGB
from ui.graphs.VerticalLabelAxis import VerticalLabelAxis  # Import the custom axis class


class ColorVariationsPlotter(QWidget):
    data_ready = QtCore.pyqtSignal(object, object, object)

    def __init__(self, parent=None):
        super(ColorVariationsPlotter, self).__init__(parent)
        self.initUI()
        self.scatter = None
        self.center_point = None  # To track the center point
        self.sample_points = []  # To track sample points
        self.sample_markers = []  # To track sample markers
        self.lines = []  # To track horizontal lines
        self.line_labels = []  # To track labels for lines
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.data_ready.connect(self.update_plot)
        self.start_calculation()
        self.lines = []  # To track horizontal lines

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.plot_widget = pg.PlotWidget(axisItems={'bottom': VerticalLabelAxis(orientation='bottom')})
        self.layout.addWidget(self.plot_widget)
        self.plot_widget.setBackground('#1F1F1F')
        self.label = QLabel(self)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def calculate_color_data(self, x_center, y_center):
        Y_values = np.linspace(0, 1, 1000)  # 1000 steps from 0 to 1 for Y
        x_flat = np.full_like(Y_values, x_center)  # Use x_center for all points
        y_flat = np.full_like(Y_values, y_center)  # Use y_center for all points

        X, Y_value, Z = xyY_to_XYZ(x_flat, y_flat, Y_values)
        R, G, B = XYZ_to_sRGB(X, Y_value, Z)

        data = np.vstack((np.zeros_like(Y_values), Y_values, R, G, B)).T  # Store Y_values as y positions
        return data

    def start_calculation(self):
        try:
            x_center, y_center, Y_actual = config.xyY_values  # Get x_center, y_center, and Y_actual from config
        except ValueError:
            self.label.setText("Invalid values in config.py. Please provide three valid numbers.")
            return

        if not (0 <= x_center <= 1) or not (0 <= y_center <= 1) or not (0 <= Y_actual <= 1):
            self.label.setText("Values in config.py must be between 0 and 1.")
            return

        future = self.executor.submit(self.calculate_color_data, x_center, y_center)
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
        y_plot = data[:, 1]  # Use Y_values as y positions
        colors = np.array([pg.mkColor((int(r), int(g), int(b))) for r, g, b in data[:, 2:5]])

        self.data_ready.emit(x_plot, y_plot, colors)

    @QtCore.pyqtSlot(object, object, object)
    def update_plot(self, x_plot, y_plot, colors):
        if self.scatter:
            self.scatter.setData(x=x_plot, y=y_plot, brush=colors, size=0.005, symbol='s', pen=None, pxMode=False)
        else:
            self.scatter = pg.ScatterPlotItem(x=x_plot, y=y_plot, brush=colors, size=0.005, symbol='s', pen=None,
                                              pxMode=False)
            self.plot_widget.addItem(self.scatter)

        # Remove the old center point if it exists
        if self.center_point:
            self.plot_widget.removeItem(self.center_point)

        # Add the small square at the actual Y value specified in config
        x_center, y_center, Y_actual = config.xyY_values
        spot_size = 0.11  # Size of the spot

        # Create a black square with a white border for the actual Y value
        self.center_point = pg.ScatterPlotItem([0], [Y_actual], size=spot_size / 10, pen=pg.mkPen('w'),
                                               brush=pg.mkBrush('k'), pxMode=False)
        self.plot_widget.addItem(self.center_point)

        # Plot sample points from config.Samples
        self.plot_sample_points()

        # Enable antialiasing for better visual quality
        self.plot_widget.setAntialiasing(True)

        # Explicitly set the range for the y-axis
        self.plot_widget.setYRange(0, 1)
        # Optionally, set the x-axis range if needed
        self.plot_widget.setXRange(0, 1)  # Adjust this as per your requirements

    def calculate_sample_color_data(self, x_center, y_center):
        Y_values = np.linspace(0, 1, 1000)  # 1000 steps from 0 to 1 for Y
        x_flat = np.full_like(Y_values, x_center)  # Use x_center for all points
        y_flat = np.full_like(Y_values, y_center)  # Use y_center for all points

        X, Y_value, Z = xyY_to_XYZ(x_flat, y_flat, Y_values)
        R, G, B = XYZ_to_sRGB(X, Y_value, Z)

        data = np.vstack((np.zeros_like(Y_values), Y_values, R, G, B)).T  # Store Y_values as y positions
        return data

    def plot_sample_points(self):
        # Clear previously plotted sample points, markers, and lines
        for sample_point in self.sample_points:
            self.plot_widget.removeItem(sample_point)
        for sample_marker in self.sample_markers:
            self.plot_widget.removeItem(sample_marker)
        for line in self.lines:
            self.plot_widget.removeItem(line)
        for label in self.line_labels:
            self.plot_widget.removeItem(label)
        self.sample_points.clear()
        self.sample_markers.clear()
        self.lines.clear()
        self.line_labels.clear()

        # Plot new sample points and markers
        for index, sample in enumerate(config.Samples):
            name = sample["name"]
            x = float(sample["x"])
            y = float(sample["y"])
            Y = float(sample["Y"])
            data = self.calculate_sample_color_data(x, y)

            x_plot = data[:, 0] + (index + 1) * 0.1  # Offset each sample bar
            y_plot = data[:, 1]  # Use Y_values as y positions
            colors = np.array([pg.mkColor((int(r), int(g), int(b))) for r, g, b in data[:, 2:5]])

            sample_scatter = pg.ScatterPlotItem(x=x_plot, y=y_plot, brush=colors, size=0.005, symbol='s', pen=None,
                                                pxMode=False)
            self.plot_widget.addItem(sample_scatter)
            self.sample_points.append(sample_scatter)

            # Add a point to indicate the exact Y value of the sample
            sample_marker = pg.ScatterPlotItem([x_plot[0]], [Y], size=0.01, pen=pg.mkPen('w'), brush=pg.mkBrush('k'),
                                               pxMode=False)
            self.plot_widget.addItem(sample_marker)
            self.sample_markers.append(sample_marker)

        # Set the sample names as the labels on the x-axis
        ticks = [(i * 0.1 + 0.1, sample["name"]) for i, sample in enumerate(config.Samples)]
        self.plot_widget.getAxis('bottom').setTicks([ticks])

        # Add horizontal dashed lines above and below the Y value
        Y_actual = config.xyY_values[2]
        luminance = config.luminance[0]
        dashed_pen = pg.mkPen(color='w')
        dashed_pen.setStyle(QtCore.Qt.CustomDashLine)
        dashed_pen.setDashPattern([4, 2])
        upper_line = pg.InfiniteLine(pos=Y_actual + luminance, angle=0, pen=dashed_pen)
        lower_line = pg.InfiniteLine(pos=Y_actual - luminance, angle=0, pen=dashed_pen)
        self.plot_widget.addItem(upper_line)
        self.plot_widget.addItem(lower_line)
        self.lines.extend([upper_line, lower_line])

        # Draw labels for the horizontal lines
        upper_label = pg.TextItem(f"{Y_actual + luminance:.3f}", color='w', anchor=(1, 1))
        lower_label = pg.TextItem(f"{Y_actual - luminance:.3f}", color='w', anchor=(1, 0))
        upper_label.setPos(self.plot_widget.viewRect().right(), Y_actual + luminance)
        lower_label.setPos(self.plot_widget.viewRect().right(), Y_actual - luminance)
        self.plot_widget.addItem(upper_label)
        self.plot_widget.addItem(lower_label)
        self.line_labels.extend([upper_label, lower_label])

