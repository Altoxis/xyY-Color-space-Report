# ui/interfaces/ReferenceSelector/layout.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLineEdit
import ui.interfaces.ReferenceSelector.functions as functions
import ui.interfaces.events as events
import style
from ui.interfaces.DraggableWidget import DraggableWidget

class ReferenceSelectorLayout(QWidget):
    def __init__(self, main_window, parent=None):
        super(ReferenceSelectorLayout, self).__init__(parent)
        self.main_window = main_window  # Store reference to the main window
        self.setAcceptDrops(True)
        self.setMinimumSize(200, 150)  # Set minimum size for visibility
        self.setStyleSheet(style.CONTENT_BOX_STYLE)

        # Create the main layout
        main_layout = QVBoxLayout(self)

        # Create the search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet(style.SEARCH_BAR_STYLE)  # Apply the search bar style
        self.search_bar.textChanged.connect(self.filter_items)
        main_layout.addWidget(self.search_bar)

        # Create the scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.container_widget = QWidget()
        self.container_widget.setStyleSheet("background-color: %s;" % style.LIGHTER_DARK_GREY)
        self.container_layout = QVBoxLayout(self.container_widget)

        self.scroll_area.setWidget(self.container_widget)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

        # Load colors from the database
        functions.load_colors_from_db(self)

    def filter_items(self, query):
        for i in range(self.container_layout.count()):
            item = self.container_layout.itemAt(i).widget()
            if isinstance(item, DraggableWidget) and query.lower() in item.text_fields[0].text().lower():
                item.show()
            else:
                item.hide()

    def dragEnterEvent(self, event):
        events.drag_enter_event(self, event)

    def dragMoveEvent(self, event):
        events.drag_move_event(self, event)

    def dropEvent(self, event):
        functions.drop_event_reference_selector(self, event)
