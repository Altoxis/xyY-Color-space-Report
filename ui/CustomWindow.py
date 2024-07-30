# CustomWindow.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from ui.graphs.XYPlotter import XYPlotter
from ui.graphs.ColorVariationsPlotter import ColorVariationsPlotter
import ui.interfaces.PlottedColor.layout as plotted_color_layout
import ui.interfaces.ReferenceSelector.layout as reference_selector_layout
import ui.interfaces.Samples.layout as samples_layout
import ui.interfaces.Measurement.layout as measurement_layout
import ui.interfaces.delete.layout as delete_layout
import ui.interfaces.menu.menu as menu
from ui.interfaces.DraggableWidget import DraggableWidget
import style
from ui.scene.layout import SceneLayout

class CustomWindow(QWidget):
    def __init__(self, parent=None):
        super(CustomWindow, self).__init__(parent)
        self.setWindowTitle('Color Management System')
        self.setGeometry(100, 100, 1600, 800)  # Adjusted the width to ensure enough space
        self.setObjectName("MainWidget")
        self.setStyleSheet(f"""
            QWidget#MainWidget {{
                background-color: {style.DARK_GREY};
            }}
            {style.SCROLL_AREA_STYLE}
        """)

        self.editable = False

        # Create the main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # First HBox for the two graph plotters and the scene
        hbox1 = QHBoxLayout()
        self.xy_plotter = XYPlotter(self)
        self.color_variations_plotter = ColorVariationsPlotter(self)
        self.color_variations_plotter.plot_widget.setYRange(0, 0.5)  # Set y-axis range from 0 to 0.5
        hbox1.addWidget(self.xy_plotter)
        hbox1.addWidget(self.color_variations_plotter)

        # Initialize the scene layout
        self.scene_layout = SceneLayout()
        self.scene_layout.view.setFixedWidth(400)
        hbox1.addWidget(self.scene_layout.view)

        # Second HBox for the first drop area and delete drop area
        hbox2 = QHBoxLayout()
        vbox2 = QVBoxLayout()
        title_plotted_color = QLabel('Plotted Color')
        title_plotted_color.setStyleSheet(style.LABEL_STYLE)
        vbox2.addWidget(title_plotted_color)
        self.drop_area1 = plotted_color_layout.PlottedColorLayout(main_window=self)
        vbox2.addWidget(self.drop_area1)

        # Add delete drop area with title above
        vbox_delete = QVBoxLayout()
        self.title_delete_area = QLabel('Delete Area')
        self.title_delete_area.setStyleSheet(style.LABEL_STYLE)
        self.title_delete_area.setVisible(False)  # Start hidden
        vbox_delete.addWidget(self.title_delete_area)
        self.delete_drop_area = delete_layout.DeleteDropArea(main_window=self)
        self.delete_drop_area.setVisible(False)  # Start hidden
        vbox_delete.addWidget(self.delete_drop_area)

        hbox2.addLayout(vbox2)
        hbox2.addLayout(vbox_delete)

        # Third HBox for the three VBoxes
        self.title_color_database = QLabel('Color Database')
        self.title_color_database.setStyleSheet(style.LABEL_STYLE)
        self.drop_area2 = reference_selector_layout.ReferenceSelectorLayout(main_window=self)

        self.title_samples = QLabel('Samples')
        self.title_samples.setStyleSheet(style.LABEL_STYLE)
        self.drop_area3 = samples_layout.SamplesLayout(main_window=self, xy_plotter=self.xy_plotter)  # Pass the main_window and XYPlotter instance

        self.title_measurements = QLabel('Measurements')
        self.title_measurements.setStyleSheet(style.LABEL_STYLE)
        self.drop_area4 = measurement_layout.MeasurementLayout(main_window=self)

        hbox3 = QHBoxLayout()
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.title_color_database)
        vbox1.addWidget(self.drop_area2)

        vbox2_2 = QVBoxLayout()
        vbox2_2.addWidget(self.title_samples)
        vbox2_2.addWidget(self.drop_area3)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.title_measurements)
        vbox3.addWidget(self.drop_area4)

        hbox3.addLayout(vbox1)
        hbox3.addLayout(vbox2_2)
        hbox3.addLayout(vbox3)

        # Add HBoxes to the main layout
        main_layout.addLayout(hbox1)
        main_layout.addLayout(hbox2)
        main_layout.addLayout(hbox3)

        # Add the menu (always visible) at the bottom
        self.menu = menu.Menu(self, main_window=self)
        main_layout.addWidget(self.menu, alignment=Qt.AlignBottom)

        # Set the main layout
        self.setLayout(main_layout)

        # Apply the main window style
        self.setStyleSheet(style.MAIN_WINDOW_STYLE + style.SCROLL_AREA_STYLE)

        # Hide menus initially
        self.hide_menus()

    def hide_menus(self):
        self.drop_area2.setVisible(False)
        self.title_color_database.setVisible(False)
        self.drop_area3.setVisible(False)
        self.title_samples.setVisible(False)
        self.drop_area4.setVisible(False)
        self.title_measurements.setVisible(False)

    def update_plotters(self):
        # Trigger updates in both plotters
        self.xy_plotter.start_calculation()
        self.color_variations_plotter.start_calculation()
        self.scene_layout.update_scene()

    def update_charts(self):
        # Refresh charts using the latest data
        self.drop_area3.update_samples_list()
        self.drop_area4.update_measurements_list()
        self.xy_plotter.start_calculation()
        self.color_variations_plotter.start_calculation()
        self.scene_layout.update_scene()

    def toggle_editable(self, editable):
        self.editable = editable
        for area in [self.drop_area1, self.drop_area2, self.drop_area3, self.drop_area4]:
            for i in range(area.container_layout.count()):
                widget = area.container_layout.itemAt(i).widget()
                if isinstance(widget, DraggableWidget):
                    for text_field in widget.text_fields:
                        text_field.setReadOnly(not editable)
                        text_field.setStyleSheet(style.LINE_EDIT_STYLE_EDITABLE if editable else style.LINE_EDIT_STYLE)
                        if editable:
                            text_field.textChanged.connect(self.update_charts)
                        else:
                            text_field.textChanged.disconnect(self.update_charts)
        self.delete_drop_area.setVisible(editable)
        self.title_delete_area.setVisible(editable)
        self.update_charts()  # Initial update when toggling
