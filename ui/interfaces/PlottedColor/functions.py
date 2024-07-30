# functions (3).py

from PyQt5.Qt import QDropEvent
from PyQt5.QtCore import Qt
import config

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
        # Trigger update in ColorVariationsPlotter
        if hasattr(self.main_window, 'xy_plotter'):
            self.main_window.xy_plotter.plot_sample_points()

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
        if hasattr(instance.main_window, 'xy_plotter'):
            instance.main_window.xy_plotter.plot_sample_points()

def replace_draggable_widget(instance, widget):
    # Clear existing widgets
    for i in reversed(range(instance.container_layout.count())):
        existing_widget = instance.container_layout.itemAt(i).widget()
        instance.container_layout.removeWidget(existing_widget)
        existing_widget.setParent(None)

    # Add new widget centered
    instance.container_layout.addWidget(widget, alignment=Qt.AlignCenter)

    # Ensure text fields are visible again
    for text_field in widget.text_fields:
        text_field.setVisible(True)

    instance.update_config_and_plot(widget)

def update_config_and_plot(instance, widget):
    # Extract data from the widget's text fields
    name = widget.text_fields[0].text()
    x = float(widget.text_fields[1].text())
    y = float(widget.text_fields[2].text())
    Y_1 = float(widget.text_fields[3].text())

    # Update config.py with the new values
    config.xyY_values = [x, y, Y_1]

    # Trigger updates in the plotters
    instance.main_window.update_plotters()  # Use the reference to main window

def drop_event_plotted_color(instance, event):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        replace_draggable_widget(instance, widget)
        widget.show()
        # Ensure update_samples_list is called after replacing the plotted color
        if hasattr(instance.main_window, 'drop_area3'):
            instance.main_window.drop_area3.update_samples_list()
        # Trigger update in ColorVariationsPlotter
        if hasattr(instance.main_window, 'xy_plotter'):
            instance.main_window.xy_plotter.plot_sample_points()
