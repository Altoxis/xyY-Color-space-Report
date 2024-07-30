from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import os
import style

class SamplesButtonLayout(QWidget):
    def __init__(self, parent=None, main_window=None):
        super(SamplesButtonLayout, self).__init__(parent)
        self.main_window = main_window
        self.setMinimumSize(50, 50)  # Set minimum size for visibility
        self.setStyleSheet(style.ICON_STYLE)

        # Create the button with icon
        self.samples_button = QPushButton(self)
        self.samples_button.setIcon(QIcon(os.path.join('resources', 'icons', 'samples.svg')))
        self.samples_button.setIconSize(QSize(32, 32))
        self.samples_button.setStyleSheet(style.ICON_STYLE)
        self.samples_button.clicked.connect(self.toggle_samples)

        # Create the main layout and add the button
        layout = QVBoxLayout(self)
        layout.addWidget(self.samples_button)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def toggle_samples(self):
        visible = not self.main_window.drop_area3.isVisible()
        self.main_window.drop_area3.setVisible(visible)
        self.main_window.title_samples.setVisible(visible)
