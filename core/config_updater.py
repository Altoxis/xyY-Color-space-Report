from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QLabel
import core.config as config
from core.func import reload_config_data

class ConfigUpdater(QWidget):
    def __init__(self, xy_plotter, color_variations_plotter, parent=None):
        super(ConfigUpdater, self).__init__(parent)
        self.xy_plotter = xy_plotter
        self.color_variations_plotter = color_variations_plotter
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.x_input = QLineEdit(self)
        self.x_input.setPlaceholderText('Enter x value (0 to 1)')
        self.x_input.textChanged.connect(self.update_config)
        self.layout.addWidget(self.x_input)

        self.y_input = QLineEdit(self)
        self.y_input.setPlaceholderText('Enter y value (0 to 1)')
        self.y_input.textChanged.connect(self.update_config)
        self.layout.addWidget(self.y_input)

        self.Y_input = QLineEdit(self)
        self.Y_input.setPlaceholderText('Enter luminance value Y (0 to 1)')
        self.Y_input.textChanged.connect(self.update_config)
        self.layout.addWidget(self.Y_input)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

    def update_config(self):
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            Y = float(self.Y_input.text())
        except ValueError:
            self.label.setText("Please enter valid numbers for x, y, and Y.")
            return

        if not (0 <= x <= 1) or not (0 <= y <= 1) or not (0 <= Y <= 1):
            self.label.setText("Values must be between 0 and 1.")
            return

        # Update the config file
        config.xyY_values = [x, y, Y]

        # Reload the plots
        reload_config_data(self.xy_plotter, self.color_variations_plotter)

        self.label.setText("Config updated and plots reloaded.")
