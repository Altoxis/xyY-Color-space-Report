from PyQt5.QtWidgets import QWidget, QHBoxLayout
from ui.interfaces.menu.edition.layout import EditButtonLayout
from ui.interfaces.menu.database.layout import DatabaseButtonLayout
from ui.interfaces.menu.samples.layout import SamplesButtonLayout
from ui.interfaces.menu.measurement.layout import MeasurementButtonLayout
import style
from PyQt5.QtCore import Qt

class Menu(QWidget):
    def __init__(self, parent=None, main_window=None):
        super(Menu, self).__init__(parent)
        self.main_window = main_window
        self.setMinimumSize(50, 50)  # Set minimum size for visibility
        self.setStyleSheet("background-color: #444444;")  # Set background color to dark grey

        # Create the main layout
        layout = QHBoxLayout(self)

        # Add menu items (e.g., EditButtonLayout)
        self.edit_button_layout = EditButtonLayout(self, main_window=self.main_window)
        layout.addWidget(self.edit_button_layout)

        # Add DatabaseButtonLayout
        self.database_button_layout = DatabaseButtonLayout(self, main_window=self.main_window)
        layout.addWidget(self.database_button_layout)

        # Add SamplesButtonLayout
        self.samples_button_layout = SamplesButtonLayout(self, main_window=self.main_window)
        layout.addWidget(self.samples_button_layout)

        # Add MeasurementButtonLayout
        self.measurement_button_layout = MeasurementButtonLayout(self, main_window=self.main_window)
        layout.addWidget(self.measurement_button_layout)

        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
