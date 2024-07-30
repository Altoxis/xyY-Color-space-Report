# ui/interfaces/Samples/layout.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import os
from PyQt5.QtCore import Qt

import ui.interfaces.Samples.functions as functions
import ui.interfaces.events as events
import style
import config
from ui.interfaces.Samples.TolerancesConfigurator import TolerancesConfigurator  # Import the new configurator
from ui.interfaces.Samples.SampleConfigurator import SampleConfigurator  # Import the SampleConfigurator
from ui.interfaces.DraggableWidget import DraggableWidget  # Import the DraggableWidget

class SamplesLayout(QWidget):
    def __init__(self, main_window, xy_plotter, parent=None):
        super(SamplesLayout, self).__init__(parent)
        self.main_window = main_window  # Store reference to the main window
        self.xy_plotter = xy_plotter  # Store the XYPlotter instance
        self.setAcceptDrops(True)
        self.setMinimumSize(100, 150)  # Set minimum size for visibility
        self.setStyleSheet(style.CONTENT_BOX_STYLE)

        # Create the tolerances button
        self.tolerances_button = QPushButton(self)
        self.tolerances_button.setIcon(QIcon(os.path.join('resources', 'icons', 'tol.svg')))
        self.tolerances_button.setIconSize(QSize(32, 32))
        self.tolerances_button.setStyleSheet(style.ICON_STYLE)
        self.tolerances_button.clicked.connect(self.open_tolerances_configurator)

        # Create the add sample button
        self.add_sample_button = QPushButton(self)
        self.add_sample_button.setIcon(QIcon(os.path.join('resources', 'icons', 'plus.svg')))
        self.add_sample_button.setIconSize(QSize(32, 32))
        self.add_sample_button.setStyleSheet(style.ICON_STYLE)
        self.add_sample_button.clicked.connect(self.open_sample_configurator)

        # Create the pantone button
        self.pantone_button = QPushButton(self)
        self.pantone_button.setIcon(QIcon(os.path.join('resources', 'icons', 'pantone.svg')))
        self.pantone_button.setIconSize(QSize(32, 32))
        self.pantone_button.setStyleSheet(style.ICON_STYLE)
        self.pantone_button.clicked.connect(self.add_closest_colors)

        # Create a horizontal layout for the buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.tolerances_button)
        buttons_layout.addWidget(self.add_sample_button)
        buttons_layout.addWidget(self.pantone_button)

        # Create scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(style.SCROLL_AREA_STYLE)

        container_widget = QWidget()
        container_widget.setStyleSheet("background-color: %s;" % style.LIGHTER_DARK_GREY)
        self.container_layout = QVBoxLayout(container_widget)

        self.scroll_area.setWidget(container_widget)
        layout = QVBoxLayout(self)
        layout.addLayout(buttons_layout)  # Add the buttons layout to the main layout
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        events.drag_enter_event(self, event)

    def dragMoveEvent(self, event):
        events.drag_move_event(self, event)

    def dropEvent(self, event):
        functions.drop_event_samples(self, event)
        self.update_samples_list()

    def update_samples_list(self):
        config.Samples.clear()  # Clear the Samples list
        for i in range(self.container_layout.count()):
            widget = self.container_layout.itemAt(i).widget()
            config.Samples.append({
                "name": widget.text_fields[0].text(),
                "x": widget.text_fields[1].text(),
                "y": widget.text_fields[2].text(),
                "Y": widget.text_fields[3].text()
            })
        print(config.Samples)
        self.xy_plotter.plot_sample_points()  # Update the plot when the samples list is updated
        self.main_window.color_variations_plotter.plot_sample_points()  # Update ColorVariationsPlotter
        self.main_window.scene_layout.update_scene()  # Update the scene

    def handle_drag_out(self):
        self.update_samples_list()

    def open_tolerances_configurator(self):
        dialog = TolerancesConfigurator(self)
        if dialog.exec_():
            print("Tolerances updated")
            self.main_window.update_charts()  # Update charts after saving tolerances

    def open_sample_configurator(self):
        dialog = SampleConfigurator(self)
        if dialog.exec_():
            name, x, y, Y = dialog.get_sample_data()
            self.add_sample_widget(name, x, y, Y)

    def add_sample_widget(self, name, x, y, Y):
        widget = DraggableWidget(self)
        widget.text_fields[0].setText(name)
        widget.text_fields[1].setText(str(x))
        widget.text_fields[2].setText(str(y))
        widget.text_fields[3].setText(str(Y))
        widget.text_fields[0].editingFinished.connect(self.main_window.update_charts)
        widget.text_fields[1].editingFinished.connect(self.main_window.update_charts)
        widget.text_fields[2].editingFinished.connect(self.main_window.update_charts)
        widget.text_fields[3].editingFinished.connect(self.main_window.update_charts)
        self.container_layout.addWidget(widget)
        self.update_samples_list()

    def add_closest_colors(self):
        functions.add_closest_colors(self)
        self.update_samples_list()
