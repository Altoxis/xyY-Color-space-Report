import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QGraphicsEllipseItem
from PyQt5.QtGui import QColor, QBrush, QPen, QFont
from PyQt5.QtCore import Qt
import config
from core.color_functions import get_closest_point_on_ellipse  # Ensure this function is defined


class EllipsePlotter:
    def __init__(self, chart):
        self.chart = chart
        self.ellipses = []
        self.lines = []
        self.distance_labels = []
        self.labels = []

    def clear(self):
        for item in self.ellipses + self.lines + self.distance_labels + self.labels:
            self.chart.removeItem(item)
        self.ellipses.clear()
        self.lines.clear()
        self.distance_labels.clear()
        self.labels.clear()

    def plot_ellipse(self, x0, y0, width, height, angle, pen, shadow_color):
        t = np.linspace(0, 2 * np.pi, 500)
        Ell = np.array([width * np.cos(t), height * np.sin(t)])
        R_rot = np.array([[np.cos(np.radians(angle)), -np.sin(np.radians(angle))],
                          [np.sin(np.radians(angle)), np.cos(np.radians(angle))]])
        Ell_rot = np.dot(R_rot, Ell)
        curve = pg.PlotCurveItem(x=x0 + Ell_rot[0], y=y0 + Ell_rot[1], pen=pen)
        self.chart.addItem(curve)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(1, 1)
        shadow.setColor(QColor(*shadow_color))
        curve.setGraphicsEffect(shadow)
        self.ellipses.append(curve)

    def plot_ellipses(self, x, y, ellipse_data):
        pen = pg.mkPen(color=QColor(*ellipse_data["pen_color"]), width=ellipse_data["pen_width"])
        self.plot_ellipse(x, y, ellipse_data["width1"], ellipse_data["height1"], ellipse_data["rotation"], pen,
                          ellipse_data["shadow_color"])
        self.plot_ellipse(x, y, ellipse_data["width2"], ellipse_data["height2"], ellipse_data["rotation"], pen,
                          ellipse_data["shadow_color"])

    def plot_selected_color(self, name, x, y, Y, plot_large_ellipses=True):
        self.clear()

        if plot_large_ellipses:
            ellipse_data = {
                "width1": config.ellipse_characteristics[0],
                "height1": config.ellipse_characteristics[1],
                "width2": config.ellipse_characteristics[2],
                "height2": config.ellipse_characteristics[3],
                "rotation": config.ellipse_characteristics[4],
                "pen_width": 2,
                "pen_color": (255, 255, 255),
                "shadow_color": (50, 50, 50)
            }
            self.plot_ellipses(x, y, ellipse_data)

        label = pg.TextItem(name, color='w', anchor=(0.5, 0))
        label.setFont(QFont("Arial", 10))
        label.setPos(x, y)
        self.chart.addItem(label)
        self.labels.append(label)

        # Plot lines from samples to the largest ellipse and labels indicating the length
        largest_ellipse = config.ellipse_characteristics
        a, b = largest_ellipse[0], largest_ellipse[1]
        rotation = np.radians(largest_ellipse[4])
        h, k = x, y

        for sample in config.Samples:
            sample_x, sample_y = float(sample["x"]), float(sample["y"])
            closest_point, min_dist = get_closest_point_on_ellipse(sample_x, sample_y, a, b, rotation, h, k)

            if min_dist > 0:  # Only draw the line if the sample is outside the ellipse
                line = pg.PlotDataItem([sample_x, closest_point[0]], [sample_y, closest_point[1]],
                                       pen=pg.mkPen(color='w', width=1))
                self.chart.addItem(line)
                self.lines.append(line)

                distance_text = f"{min_dist:.4f}"
                distance_label = pg.TextItem(distance_text, color='w', anchor=(0, 0.5))
                distance_label.setFont(QFont("Arial", 10))
                mid_x = (sample_x + closest_point[0]) / 2
                mid_y = (sample_y + closest_point[1]) / 2
                distance_label.setPos(mid_x, mid_y)
                self.chart.addItem(distance_label)
                self.distance_labels.append(distance_label)

                ellipse_size = 0.0001
                closest_ellipse_point = QGraphicsEllipseItem(closest_point[0] - ellipse_size / 2,
                                                             closest_point[1] - ellipse_size / 2, ellipse_size,
                                                             ellipse_size)
                closest_ellipse_point.setBrush(QBrush(Qt.white))
                closest_ellipse_point.setPen(QPen(Qt.NoPen))
                self.chart.addItem(closest_ellipse_point)
                self.ellipses.append(closest_ellipse_point)
