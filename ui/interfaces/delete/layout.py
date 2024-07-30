# layout.py (DeleteDropArea class)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import ui.interfaces.delete.functions as functions
import ui.interfaces.events as events
import style
import os

class DeleteDropArea(QWidget):
    def __init__(self, parent=None, main_window=None):
        super(DeleteDropArea, self).__init__(parent)
        self.main_window = main_window  # Store reference to the main window
        self.setAcceptDrops(True)
        self.setMinimumSize(150, 90)  # Set minimum size for visibility
        self.setMaximumSize(500, 100)  # Set minimum size for visibility
        self.setStyleSheet(style.DELETE_DROP_AREA_STYLE)  # Set background color to light red

        # Create the container widget and layout
        container_widget = QWidget(self)
        container_widget.setStyleSheet(style.DELETE_DROP_AREA_STYLE)
        self.container_layout = QVBoxLayout(container_widget)
        self.container_layout.setAlignment(Qt.AlignCenter)  # Center the contents

        # Create the main layout and add the container widget
        layout = QVBoxLayout(self)
        layout.addWidget(container_widget)
        self.setLayout(layout)

        # Add the delete icon inside the zone
        self.delete_icon = QLabel(self)
        self.delete_icon.setPixmap(QPixmap(os.path.join('resources', 'icons', 'delete.svg')).scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.delete_icon.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.delete_icon)

    def dragEnterEvent(self, event):
        events.drag_enter_event(self, event)
        self.setStyleSheet(style.DELETE_DROP_AREA_HOVER_STYLE)

    def dragLeaveEvent(self, event):
        self.setStyleSheet(style.DELETE_DROP_AREA_STYLE)

    def dragMoveEvent(self, event):
        events.drag_move_event(self, event)

    def dropEvent(self, event):
        functions.drop_event_delete(self, event)
        self.setStyleSheet(style.DELETE_DROP_AREA_STYLE)
