# layout.py (PlottedColorLayout class)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt
import ui.interfaces.PlottedColor.functions as functions
import ui.interfaces.events as events
from ui.interfaces.DraggableWidget import DraggableWidget
import style
import config

class PlottedColorLayout(QWidget):
    def __init__(self, parent=None, main_window=None):
        super(PlottedColorLayout, self).__init__(parent)
        self.main_window = main_window  # Store reference to the main window
        self.setAcceptDrops(True)
        self.setMinimumSize(150, 90)  # Set minimum size for visibility
        self.setMaximumSize(900, 100)  # Set minimum size for visibility
        self.setStyleSheet("background-color: %s;" % style.LIGHTER_GREY)  # Set background color to light grey
        self.setStyleSheet(style.CONTENT_BOX_STYLE)
        # Create the container widget and layout
        container_widget = QWidget(self)
        container_widget.setStyleSheet("background-color: %s;" % style.LIGHTER_DARK_GREY)
        self.container_layout = QVBoxLayout(container_widget)
        self.container_layout.setAlignment(Qt.AlignCenter)  # Center the contents

        # Create the main layout and add the container widget
        layout = QVBoxLayout(self)
        layout.addWidget(container_widget)
        self.setLayout(layout)

        # Initialize with a draggable widget from config
        self.initialize_draggable_widget()

    def initialize_draggable_widget(self):
        widget = DraggableWidget(self)
        widget.text_fields[0].setText(config.initial_widget_name)
        widget.text_fields[1].setText(str(config.xyY_values[0]))
        widget.text_fields[2].setText(str(config.xyY_values[1]))
        widget.text_fields[3].setText(str(config.xyY_values[2]))
        self.container_layout.addWidget(widget)
        widget.valuesChanged.connect(self.replot_with_new_values)

    def dragEnterEvent(self, event):
        events.drag_enter_event(self, event)

    def dragMoveEvent(self, event):
        events.drag_move_event(self, event)

    def dropEvent(self, event):
        functions.drop_event_plotted_color(self, event)
        widget = event.source()
        if isinstance(widget, DraggableWidget):
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Ensure it expands to full width
            widget.resize(self.width(), widget.height())  # Resize to the width of the drop area

            # Set fixed size for the name textbox
            name_textbox = widget.text_fields[0]  # Assuming the first textbox is the name textbox
            name_textbox.setFixedWidth(230)  # Set a fixed width for the name textbox

            self.container_layout.addWidget(widget)  # Add the widget to the layout
            self.container_layout.setAlignment(widget, Qt.AlignCenter)  # Align the widget to the center

            widget.valuesChanged.connect(self.replot_with_new_values)

    def replace_draggable_widget(self, widget):
        functions.replace_draggable_widget(self, widget)
        widget.valuesChanged.connect(self.replot_with_new_values)

    def update_config_and_plot(self, widget):
        functions.update_config_and_plot(self, widget)

    def replot_with_new_values(self):
        for i in range(self.container_layout.count()):
            widget = self.container_layout.itemAt(i).widget()
            if isinstance(widget, DraggableWidget):
                functions.update_config_and_plot(self, widget)
