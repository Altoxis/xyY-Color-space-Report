from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QBrush, QColor
from .functions import plot_color, plot_sample_color, plot_delta
import config
from core.color_functions import color_difference

class SceneLayout:
    def __init__(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("background-color: #1F1F1F; border: none;")  # Set background to dark grey and remove borders
        self.update_scene()

    def update_scene(self):
        self.scene.clear()

        # Plot the main color
        x_center, y_center, Y = config.xyY_values
        plot_color(x_center, y_center, Y, "Main Color", self.scene, 10, 10)

        # Plot sample colors and their differences
        y_offset = 60
        for sample in config.Samples:
            name = sample["name"]
            x, y, Y = sample["x"], sample["y"], sample["Y"]
            plot_sample_color(x, y, Y, name, self.scene, 10, y_offset)
            y_offset += 50
