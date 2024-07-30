import os
import config
from ui.interfaces.DraggableWidget import DraggableWidget
from core.color_functions import find_closest_colors

def drop_event_samples(instance, event):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        for text_field in widget.text_fields:
            text_field.setVisible(True)
        instance.container_layout.addWidget(widget)
        widget.show()
        instance.update_samples_list()
        instance.main_window.color_variations_plotter.plot_sample_points()
        instance.main_window.scene_layout.update_scene()

def add_closest_colors(instance):
    db_path = os.path.join('resources', 'database', 'colors.db')

    # Use the xyY_values from the config file as the plotted color
    main_color = (0, *config.xyY_values)

    # Find the 5 closest colors
    closest_colors = find_closest_colors(main_color, db_path, n=5)

    for color in closest_colors:
        name, x, y, Y = color
        widget = DraggableWidget(instance)
        widget.text_fields[0].setText(name)
        widget.text_fields[1].setText(str(x))
        widget.text_fields[2].setText(str(y))
        widget.text_fields[3].setText(str(Y))
        widget.text_fields[0].editingFinished.connect(instance.main_window.update_charts)
        widget.text_fields[1].editingFinished.connect(instance.main_window.update_charts)
        widget.text_fields[2].editingFinished.connect(instance.main_window.update_charts)
        widget.text_fields[3].editingFinished.connect(instance.main_window.update_charts)
        instance.container_layout.addWidget(widget)
