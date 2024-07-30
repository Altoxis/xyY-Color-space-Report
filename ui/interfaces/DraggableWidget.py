from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData
from PyQt5.QtGui import QMouseEvent, QDrag, QPixmap
import style

class DraggableWidget(QWidget):
    valuesChanged = pyqtSignal()

    def __init__(self, parent=None):
        super(DraggableWidget, self).__init__(parent)
        self.setAcceptDrops(False)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.layout.setSpacing(5)

        self.text_fields = [QLineEdit(self) for _ in range(4)]

        for text_field in self.text_fields:
            text_field.setFixedHeight(40)
            text_field.setStyleSheet(style.LINE_EDIT_STYLE)
            text_field.setReadOnly(True)  # Set text fields to read-only by default
            text_field.textChanged.connect(self.on_value_changed)
            text_field.installEventFilter(self)  # Install event filter to handle drag
            self.layout.addWidget(text_field)

        self.setFixedHeight(50)
        self.setStyleSheet(style.DRAGGABLE_WIDGET_STYLE)
        self.startPos = None

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.startPos:
            distance = (event.pos() - self.startPos).manhattanLength()
            if distance >= QApplication.startDragDistance():
                self.start_drag()

    def start_drag(self):
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setData('application/x-draggablewidget', b'')  # Custom MIME type
        drag.setMimeData(mime_data)

        pixmap = QPixmap(self.size())
        self.render(pixmap)

        drag.setPixmap(pixmap)
        drag.setHotSpot(self.startPos)

        self.setWindowOpacity(0.25)
        drag.exec_(Qt.MoveAction)
        self.setWindowOpacity(1.0)

    def on_value_changed(self):
        self.valuesChanged.emit()

    def eventFilter(self, source, event):
        if event.type() == QMouseEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            self.startPos = event.pos()
        elif event.type() == QMouseEvent.MouseMove and event.buttons() == Qt.LeftButton:
            if self.startPos and (event.pos() - self.startPos).manhattanLength() >= QApplication.startDragDistance():
                self.start_drag()
        return super(DraggableWidget, self).eventFilter(source, event)
