from PyQt5.QtGui import QColor, QBrush, QPen, QFont
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt
import numpy as np
import config
from core.color_functions import xyY_to_XYZ, XYZ_to_sRGB, color_difference, get_closest_point_on_ellipse


def calculate_color(x, y, Y):
    x = float(x)
    y = float(y)
    Y = float(Y)
    X, Y_value, Z = xyY_to_XYZ(x, y, Y)
    R, G, B = XYZ_to_sRGB(X, Y_value, Z)
    return QColor(R, G, B)


def plot_color(x, y, Y, name, scene, pos_x, pos_y):
    x = float(x)
    y = float(y)
    Y = float(Y)
    color = calculate_color(x, y, Y)
    rect = QGraphicsRectItem(pos_x, pos_y, 40, 40)
    rect.setBrush(QBrush(color))
    scene.addItem(rect)

    text = QGraphicsTextItem(name)
    text.setPos(pos_x + 50, pos_y)
    text.setDefaultTextColor(Qt.white)
    scene.addItem(text)


def plot_sample_color(x, y, Y, name, scene, pos_x, pos_y):
    plot_color(x, y, Y, name, scene, pos_x, pos_y)

    # Add delta check
    delta = calculate_delta(x, y, Y)
    plot_delta(delta, x, y, Y, scene, pos_x + 50, pos_y + 20)


def calculate_delta(x, y, Y):
    x = float(x)
    y = float(y)
    Y = float(Y)
    return color_difference((0, config.xyY_values[0], config.xyY_values[1], config.xyY_values[2]), (0, x, y, Y))


def plot_delta(delta, x, y, Y, scene, pos_x, pos_y):
    delta = float(delta)
    delta_text = QGraphicsTextItem(f"Δ: {delta:.2f}")
    delta_text.setPos(pos_x, pos_y)  # Adjust to place next to delta
    delta_text.setDefaultTextColor(Qt.white)
    scene.addItem(delta_text)

    # Check pass/fail status
    status, color = check_pass_fail(x, y, Y)
    status_text = QGraphicsTextItem(status)
    status_text.setPos(pos_x + 70, pos_y)  # Adjust to place next to delta
    status_text.setDefaultTextColor(color)
    scene.addItem(status_text)


def check_pass_fail(x, y, Y):
    x = float(x)
    y = float(y)
    Y = float(Y)

    h, k = config.xyY_values[:2]
    vector_x = x - h
    vector_y = y - k
    angle = np.arctan2(vector_y, vector_x)
    distance = np.hypot(vector_x, vector_y)

    def ellipse_distance(a, b, angle, rotation):
        cos_angle = np.cos(angle - rotation)
        sin_angle = np.sin(angle - rotation)
        return a * b / np.sqrt((b * cos_angle) ** 2 + (a * sin_angle) ** 2)

    small_ellipse = config.ellipse_characteristics[2:4]
    large_ellipse = config.ellipse_characteristics[:2]
    rotation = np.radians(config.ellipse_characteristics[4])

    small_ellipse_dist = ellipse_distance(small_ellipse[0], small_ellipse[1], angle, rotation)
    large_ellipse_dist = ellipse_distance(large_ellipse[0], large_ellipse[1], angle, rotation)

    within_small_ellipse = distance <= small_ellipse_dist
    within_large_ellipse = distance <= large_ellipse_dist

    # Check if the color is within the luminosity range
    luminosity_range = config.luminance[0]
    within_luminosity = abs(config.xyY_values[2] - Y) <= luminosity_range

    if within_small_ellipse and within_luminosity:
        return "Pass", QColor("green")
    elif within_large_ellipse and within_luminosity:
        return "Pass", QColor("orange")
    else:
        return "Fail", QColor("red")
