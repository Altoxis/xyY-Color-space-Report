from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import os
import style

class DatabaseButtonLayout(QWidget):
    def __init__(self, parent=None, main_window=None):
        super(DatabaseButtonLayout, self).__init__(parent)
        self.main_window = main_window
        self.setMinimumSize(50, 50)  # Set minimum size for visibility
        self.setStyleSheet(style.ICON_STYLE)

        # Create the button with icon
        self.db_button = QPushButton(self)
        self.db_button.setIcon(QIcon(os.path.join('resources', 'icons', 'database.svg')))
        self.db_button.setIconSize(QSize(32, 32))
        self.db_button.setStyleSheet(style.ICON_STYLE)
        self.db_button.clicked.connect(self.toggle_database)

        # Create the main layout and add the button
        layout = QVBoxLayout(self)
        layout.addWidget(self.db_button)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def toggle_database(self):
        visible = not self.main_window.drop_area2.isVisible()
        self.main_window.drop_area2.setVisible(visible)
        self.main_window.title_color_database.setVisible(visible)
