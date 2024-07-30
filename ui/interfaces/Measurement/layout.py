from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
import os
import pyqtgraph as pg
import style
import config
from ui.interfaces.Measurement.functions import MeasurementFunctions
from ui.interfaces.DraggableWidget import DraggableWidget
from core.color_functions import xyY_to_XYZ, XYZ_to_sRGB

class MeasurementLayout(QWidget):
    def __init__(self, main_window, parent=None):
        super(MeasurementLayout, self).__init__(parent)
        self.main_window = main_window
        self.measurement_functions = MeasurementFunctions(self)
        self.measurement_counter = 0
        self.measurements = []
        self.sample_labels = {}
        self.name_editors = {}
        self.current_editing_sample_id = None
        self.plots = {}  # To store the plot references

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Keep the existing button
        self.button = QPushButton('Listen to YS3010')
        self.button.setStyleSheet(style.BUTTON_STYLE)
        self.button.clicked.connect(self.measurement_functions.start_listening)
        layout.addWidget(self.button)

        self.setStyleSheet(style.CONTENT_BOX_STYLE)

        self.label = QLabel('')
        self.label.setObjectName("MeasurementLabel")  # Set a unique object name for the label
        self.label.setStyleSheet("""
            QLabel#MeasurementLabel {
                color: white; 
                font-size: 10pt; 
                background-color: #1F1F1F;  /* Set background color to dark grey */
                border-radius: 5px;  /* Optional: add some border radius for a smoother look */
                padding: 5px;  /* Optional: add some padding for better appearance */
            }
        """)
        layout.addWidget(self.label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.label_state = 0

        # Create a scroll area for measurements
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(style.SCROLL_AREA_STYLE)

        # Create a container widget for the scroll area content
        container_widget = QWidget()
        container_widget.setStyleSheet("background-color: %s;" % style.LIGHTER_DARK_GREY)
        self.container_layout = QVBoxLayout(container_widget)
        self.container_layout.setSpacing(10)
        self.container_layout.setContentsMargins(5, 5, 5, 5)

        self.scroll_area.setWidget(container_widget)
        layout.addWidget(self.scroll_area)

        # Create the graph widget for plotting the spectrum data
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground("#1F1F1F")
        self.graph_widget.setTitle("Spectrum Data", color="w", size="12pt")
        self.graph_widget.getAxis('left').setPen(pg.mkPen('w'))
        self.graph_widget.getAxis('bottom').setPen(pg.mkPen('w'))
        self.graph_widget.getAxis('left').setTextPen(pg.mkPen('w'))
        self.graph_widget.getAxis('bottom').setTextPen(pg.mkPen('w'))

        # Set background for the graph container
        self.graph_container = QWidget()
        self.graph_container.setStyleSheet("background-color: #1F1F1F; border-radius: 10px;")
        graph_layout = QVBoxLayout(self.graph_container)
        graph_layout.addWidget(self.graph_widget)
        layout.addWidget(self.graph_container)

        self.setLayout(layout)

    def update_label(self):
        states = ["Listening to measurement...", "Listening to measurement..", "Listening to measurement."]
        self.label.setText(states[self.label_state])
        self.label_state = (self.label_state + 1) % 3

    def add_measurement_widget(self, name, x, y, Y, spectrum_data):
        widget = DraggableWidget(self)
        widget.text_fields[0].setText(name)
        widget.text_fields[1].setText(str(x))
        widget.text_fields[2].setText(str(y))
        widget.text_fields[3].setText(str(Y / 100))
        widget.text_fields[0].editingFinished.connect(lambda: self.update_plot_on_edit(widget))
        widget.text_fields[1].editingFinished.connect(lambda: self.update_plot_on_edit(widget))
        widget.text_fields[2].editingFinished.connect(lambda: self.update_plot_on_edit(widget))
        widget.text_fields[3].editingFinished.connect(lambda: self.update_plot_on_edit(widget))
        self.container_layout.addWidget(widget)
        self.update_measurements_list()

        # Update the spectrum plot with the new measurement
        self.plot_spectrum_data(name, x, y, Y, spectrum_data)

    def update_measurements_list(self):
        config.measurement.clear()
        for i in range(self.container_layout.count()):
            widget = self.container_layout.itemAt(i).widget()
            if isinstance(widget, DraggableWidget):
                name = widget.text_fields[0].text()
                x = float(widget.text_fields[1].text())
                y = float(widget.text_fields[2].text())
                Y = float(widget.text_fields[3].text())
                spectrum_data = self.get_spectrum_data_for_name(name)
                if spectrum_data:
                    config.measurement.append((name, x, y, Y, spectrum_data))

        self.main_window.color_variations_plotter.plot_sample_points()
        self.main_window.xy_plotter.plot_sample_points()
        self.update_graph()

    def plot_spectrum_data(self, name, x, y, Y, spectrum_data):
        wavelengths = list(range(400, 400 + 10 * len(spectrum_data), 10))

        # Convert xyY to RGB to get the line color
        X, Y_value, Z = xyY_to_XYZ(x, y, Y / 100)
        R, G, B = XYZ_to_sRGB(X, Y_value, Z)
        color = QColor(R, G, B)

        # Plot the spectrum data with the corresponding color
        curve = self.graph_widget.plot(wavelengths, spectrum_data, pen=pg.mkPen(color=color, width=2))
        self.plots[name] = curve

    def update_graph(self):
        self.graph_widget.clear()
        for name, x, y, Y, spectrum_data in config.measurement:
            self.plot_spectrum_data(name, x, y, Y, spectrum_data)

    def get_spectrum_data_for_name(self, name):
        for sample_name, x, y, Y, spectrum_data in config.measurement:
            if sample_name == name:
                return spectrum_data
        return None

    def update_plot_on_edit(self, widget):
        name = widget.text_fields[0].text()
        x = float(widget.text_fields[1].text())
        y = float(widget.text_fields[2].text())
        Y = float(widget.text_fields[3].text())
        spectrum_data = self.get_spectrum_data_for_name(name)
        if spectrum_data:
            self.plot_spectrum_data(name, x, y, Y, spectrum_data)
