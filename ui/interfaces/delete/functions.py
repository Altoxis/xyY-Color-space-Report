# functions.py

from PyQt5.Qt import QDropEvent

def drag_enter_event(self, event):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()

def drop_event(self, event):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        widget.setParent(None)
        widget.deleteLater()
        if hasattr(self.main_window, 'drop_area3'):
            self.main_window.drop_area3.update_samples_list()

def drop_event_delete(instance, event: QDropEvent):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        widget.setParent(None)
        widget.deleteLater()
        # Ensure update_samples_list is called after deletion
        if hasattr(instance.main_window, 'drop_area3'):
            instance.main_window.drop_area3.update_samples_list()
        # Trigger update in ColorVariationsPlotter
        #instance.main_window.xy_plotter.plot_sample_points()
