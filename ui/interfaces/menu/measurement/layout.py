from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import os
import style

class MeasurementButtonLayout(QWidget):
    def __init__(self, parent=None, main_window=None):
        super(MeasurementButtonLayout, self).__init__(parent)
        self.main_window = main_window
        self.setMinimumSize(50, 50)  # Set minimum size for visibility
        self.setStyleSheet(style.ICON_STYLE)

        # Create the button with icon
        self.measurement_button = QPushButton(self)
        self.measurement_button.setIcon(QIcon(os.path.join('resources', 'icons', 'measurement.svg')))
        self.measurement_button.setIconSize(QSize(32, 32))
        self.measurement_button.setStyleSheet(style.ICON_STYLE)
        self.measurement_button.clicked.connect(self.toggle_measurement)

        # Create the main layout and add the button
        layout = QVBoxLayout(self)
        layout.addWidget(self.measurement_button)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def toggle_measurement(self):
        visible = not self.main_window.drop_area4.isVisible()
        self.main_window.drop_area4.setVisible(visible)
        self.main_window.title_measurements.setVisible(visible)
