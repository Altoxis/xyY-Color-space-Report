import numpy as np
import sqlite3

def xyY_to_XYZ(x, y, Y):
    X = np.where(y != 0, (x * Y) / y, 0)
    Z = np.where(y != 0, ((1 - x - y) * Y) / y, 0)
    return X, Y, Z

def XYZ_to_sRGB(X, Y, Z, gamma=1.6):
    R = 3.2406 * X - 1.5372 * Y - 0.4986 * Z
    G = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
    B = 0.0557 * X - 0.2040 * Y + 1.0570 * Z

    R = np.clip(R, 0, None)
    G = np.clip(G, 0, None)
    B = np.clip(B, 0, None)

    R = np.where(R > 0.0031308, 1.055 * (R ** (1 / gamma)) - 0.055, 12.92 * R)
    G = np.where(G > 0.0031308, 1.055 * (G ** (1 / gamma)) - 0.055, 12.92 * G)
    B = np.where(B > 0.0031308, 1.055 * (B ** (1 / gamma)) - 0.055, 12.92 * B)

    R = np.clip(R, 0, 1)
    G = np.clip(G, 0, 1)
    B = np.clip(B, 0, 1)

    R = (R * 255).astype(int)
    G = (G * 255).astype(int)
    B = (B * 255).astype(int)

    return R, G, B

def xyY_to_Lab(x, y, Y):
    X, Y, Z = xyY_to_XYZ(x, y, Y)

    Xn, Yn, Zn = 95.047, 100.0, 108.883
    X /= Xn
    Y /= Yn
    Z /= Zn

    def f(t):
        delta = 6 / 29
        if t > delta ** 3:
            return t ** (1 / 3)
        else:
            return t / (3 * delta ** 2) + 4 / 29

    L = 116 * f(Y) - 16
    a = 500 * (f(X) - f(Y))
    b = 200 * (f(Y) - f(Z))

    return L, a, b

def color_difference(color1, color2, wx=1, wy=1, wY=2):
    x1, y1, Y1 = color1[1:]
    x2, y2, Y2 = color2[1:]
    return np.sqrt(wx * (x1 - x2) ** 2 + wy * (y1 - y2) ** 2 + wY * (Y1 - Y2) ** 2)

def find_closest_colors(main_color, db_path, n=5, wx=1, wy=1, wY=2):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name, x, y, Y_1 FROM color_data")
    reference_colors = cursor.fetchall()

    differences = []
    main_color_values = main_color[1:]

    for row in reference_colors:
        name, x, y, Y = row
        reference_color = (0, float(x), float(y), float(Y))

        if (float(x), float(y), float(Y)) == tuple(main_color_values):
            continue

        difference = color_difference((0, *main_color_values), reference_color, wx, wy, wY)
        differences.append((difference, name, x, y, Y))

    differences.sort()
    closest_colors = differences[:n]
    conn.close()
    return [(name, x, y, Y) for _, name, x, y, Y in closest_colors]

def get_closest_point_on_ellipse(px, py, a, b, rotation, h, k):
    def distance_to_ellipse_point(angle):
        x_ell, y_ell = calculate_ellipse_point(a, b, angle, rotation, h, k)
        return np.hypot(px - x_ell, py - y_ell)

    angles = np.linspace(0, 2 * np.pi, 360)
    distances = [distance_to_ellipse_point(angle) for angle in angles]

    min_dist_index = np.argmin(distances)
    closest_angle = angles[min_dist_index]
    closest_point = calculate_ellipse_point(a, b, closest_angle, rotation, h, k)

    return closest_point, distances[min_dist_index]

def calculate_ellipse_point(a, b, angle, rotation, h, k):
    x = a * np.cos(angle)
    y = b * np.sin(angle)

    x_rot = x * np.cos(rotation) - y * np.sin(rotation)
    y_rot = x * np.sin(rotation) + y * np.cos(rotation)

    return x_rot + h, y_rot + k
