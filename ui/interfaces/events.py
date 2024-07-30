from PyQt5.Qt import QDragEnterEvent, QDropEvent, QDragMoveEvent
from PyQt5.QtCore import Qt
from ui.interfaces.DraggableWidget import DraggableWidget
import style

def drag_enter_event(self, event: QDragEnterEvent):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()

def drag_move_event(self, event: QDragMoveEvent):
    event.acceptProposedAction()

def drop_event_reference_selector(instance, event: QDropEvent):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        new_widget = DraggableWidget(instance.container_widget)
        for i, text_field in enumerate(widget.text_fields):
            new_widget.text_fields[i].setText(text_field.text())
        instance.container_layout.addWidget(new_widget)
        new_widget.show()

def drop_event_samples(instance, event: QDropEvent):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        for text_field in widget.text_fields:
            text_field.setVisible(True)
        instance.container_layout.addWidget(widget)
        widget.show()

def drop_event_measurement(instance, event: QDropEvent):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        widget = event.source()
        if hasattr(widget, 'parent') and hasattr(instance, 'container_widget') and widget.parent() == instance.container_widget:
            event.acceptProposedAction()
            for text_field in widget.text_fields:
                text_field.setVisible(True)
            instance.container_layout.addWidget(widget)
            widget.show()
        else:
            event.ignore()

def drop_event_plotted_color(instance, event: QDropEvent):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        instance.container_layout.addWidget(widget, alignment=Qt.AlignCenter)
        widget.show()

def drop_event_delete(instance, event: QDropEvent):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        widget.setParent(None)
        widget.deleteLater()

def toggle_editable(main_window, editable):
    new_style = style.LINE_EDIT_STYLE_EDITABLE if editable else style.LINE_EDIT_STYLE
    for area in [main_window.drop_area1, main_window.drop_area2, main_window.drop_area3, main_window.drop_area4]:
        for i in range(area.container_layout.count()):
            widget = area.container_layout.itemAt(i).widget()
            if isinstance(widget, DraggableWidget):
                for text_field in widget.text_fields:
                    text_field.setReadOnly(not editable)
                    text_field.setStyleSheet(new_style)
    main_window.delete_drop_area.setVisible(editable)
