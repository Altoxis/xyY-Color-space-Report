import sqlite3
import os
import pandas as pd
from PyQt5.QtGui import QIcon
from ui.interfaces.DraggableWidget import DraggableWidget
from core.color_functions import color_difference
import config
def load_colors_from_db(instance):
    conn = sqlite3.connect('resources/database/colors.db')
    query = "SELECT name, x, y, Y_1 FROM color_data"
    df = pd.read_sql(query, conn)
    conn.close()

    for index, row in df.iterrows():
        draggable_widget = create_draggable_widget(row)
        instance.container_layout.addWidget(draggable_widget)

def create_draggable_widget(row):
    widget = DraggableWidget()
    widget.text_fields[0].setText(row['name'])
    widget.text_fields[1].setText(str(row['x']))
    widget.text_fields[2].setText(str(row['y']))
    widget.text_fields[3].setText(str(row['Y_1']))
    return widget

def drop_event_samples(instance, event):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        for text_field in widget.text_fields:
            text_field.setVisible(True)
        instance.container_layout.addWidget(widget)
        widget.show()
        instance.update_samples_list()
        # Trigger update in ColorVariationsPlotter and the scene
        instance.main_window.color_variations_plotter.plot_sample_points()
        instance.main_window.scene_layout.update_scene()

def add_closest_colors(instance):
    db_path = os.path.join('resources', 'database', 'colors.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verify that the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='color_data';")
    table_exists = cursor.fetchone()

    if not table_exists:
        print("Error: 'color_data' table does not exist in the database.")
        conn.close()
        return

    # Use the xyY_values from the config file as the plotted color
    x_plotted, y_plotted, Y_plotted = config.xyY_values

    # Query to get all colors from the database
    cursor.execute("SELECT name, x, y, Y_1 FROM color_data")
    colors = cursor.fetchall()

    # Calculate distances and find the 5 closest colors
    closest_colors = sorted(colors, key=lambda c: color_difference((0, x_plotted, y_plotted, Y_plotted), (0, float(c[1]), float(c[2]), float(c[3]))))[:5]

    for color in closest_colors:
        widget = DraggableWidget(instance)
        widget.text_fields[0].setText(color[0])
        widget.text_fields[1].setText(str(color[1]))
        widget.text_fields[2].setText(str(color[2]))
        widget.text_fields[3].setText(str(color[3]))
        widget.text_fields[0].editingFinished.connect(instance.main_window.update_charts)
        widget.text_fields[1].editingFinished.connect(instance.main_window.update_charts)
        widget.text_fields[2].editingFinished.connect(instance.main_window.update_charts)
        widget.text_fields[3].editingFinished.connect(instance.main_window.update_charts)
        instance.container_layout.addWidget(widget)

    conn.close()

def add_color_to_db(name, x, y, Y):
    db_path = os.path.join('resources', 'database', 'colors.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO color_data (name, x, y, Y_1) VALUES (?, ?, ?, ?)", (name, x, y, Y))
    conn.commit()
    conn.close()

def delete_color_from_db(name):
    db_path = os.path.join('resources', 'database', 'colors.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM color_data WHERE name=?", (name,))
    conn.commit()
    conn.close()

def drop_event_reference(instance, event):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        name = widget.text_fields[0].text()
        x = widget.text_fields[1].text()
        y = widget.text_fields[2].text()
        Y = widget.text_fields[3].text()
        add_color_to_db(name, x, y, Y)
        instance.update_reference_list()

def drop_event_delete(instance, event):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        name = widget.text_fields[0].text()
        delete_color_from_db(name)
        instance.update_reference_list()

def drop_event(instance, event):
    if event.mimeData().hasFormat('application/x-draggablewidget'):
        event.acceptProposedAction()
        widget = event.source()
        if widget.parent() is not instance:
            widget.setParent(instance)
            instance.container_layout.addWidget(widget)
            instance.update_samples_list()
            widget.show()
        # Keep the widget in the scrollable area
        instance.scroll_area.setWidgetResizable(True)
