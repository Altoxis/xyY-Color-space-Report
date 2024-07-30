import time
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize, QRunnable, QThreadPool, pyqtSlot, QObject, pyqtSignal
import os
import style
import ui.interfaces.events as events

class WorkerSignals(QObject):
    finished = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)
        self.signals.finished.emit()

class EditButtonLayout(QWidget):
    def __init__(self, parent=None, main_window=None):
        super(EditButtonLayout, self).__init__(parent)
        self.main_window = main_window
        self.threadpool = QThreadPool()
        self.setMinimumSize(50, 50)  # Set minimum size for visibility
        self.setStyleSheet(style.ICON_STYLE)

        # Create the button with icon
        self.lock_button = QPushButton(self)
        self.lock_button.setIcon(QIcon(os.path.join('resources', 'icons', 'edit.svg')))
        self.lock_button.setIconSize(QSize(32, 32))
        self.lock_button.setStyleSheet(style.ICON_STYLE)
        self.lock_button.clicked.connect(self.toggle_editable)

        # Create the main layout and add the button
        layout = QVBoxLayout(self)
        layout.addWidget(self.lock_button)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def toggle_editable(self):
        overall_start_time = time.time()

        start_time = time.time()
        self.main_window.editable = not self.main_window.editable
        events.toggle_editable(self.main_window, self.main_window.editable)
        icon_path = 'resources/icons/edit.svg' if not self.main_window.editable else 'resources/icons/lock.svg'
        self.lock_button.setIcon(QIcon(os.path.join(icon_path)))
        print(f"Toggle editable state and icon update: {time.time() - start_time:.4f} seconds")

        start_time = time.time()
        self.main_window.delete_drop_area.setVisible(self.main_window.editable)
        print(f"Delete drop area visibility: {time.time() - start_time:.4f} seconds")

        start_time = time.time()
        widgets = [self.main_window.drop_area3.container_layout.itemAt(i).widget()
                   for i in range(self.main_window.drop_area3.container_layout.count())]
        print(f"Collecting widgets: {time.time() - start_time:.4f} seconds")

        def update_text_fields():
            for widget in widgets:
                for text_field in widget.text_fields:
                    if text_field.isReadOnly() != (not self.main_window.editable):
                        text_field.setReadOnly(not self.main_window.editable)
                        if self.main_window.editable:
                            text_field.textChanged.connect(self.main_window.update_charts)
                        else:
                            text_field.textChanged.disconnect(self.main_window.update_charts)

        worker = Worker(update_text_fields)
        worker.signals.finished.connect(self.on_worker_finished)
        self.threadpool.start(worker)
        print(f"Updating text fields: {time.time() - start_time:.4f} seconds")

        start_time = time.time()
        self.main_window.update_charts()
        print(f"Initial chart update: {time.time() - start_time:.4f} seconds")

        print(f"Overall toggle editable execution time: {time.time() - overall_start_time:.4f} seconds")

    def on_worker_finished(self):
        print("Worker task finished")

# Assuming main_window is already defined and properly set up
# main_window = ...

# EditButtonLayout can be used as follows:
# edit_button_layout = EditButtonLayout(main_window=main_window)
# main_window.some_layout.addWidget(edit_button_layout)
