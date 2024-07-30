from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt
import config


class TolerancesConfigurator(QDialog):
    def __init__(self, parent=None):
        super(TolerancesConfigurator, self).__init__(parent)
        self.setWindowTitle('')  # Remove the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 300, 200)
        self.parent = parent

        self.setStyleSheet("""
            QLabel {
                color: white;
            }
            QLabel[bold=true] {
                font-weight: bold;
            }
            QLineEdit {
                background-color: #333333;
                color: white;
            }
            QPushButton {
                background-color: #444444;
                color: white;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)

        self.layout = QVBoxLayout(self)

        self.ellipse1_widget, self.ellipse1_inputs = self.create_ellipse_inputs('Ellipse 1')
        self.ellipse2_widget, self.ellipse2_inputs = self.create_ellipse_inputs('Ellipse 2')
        self.rotation_widget = self.create_rotation_input()  # Create rotation input separately

        self.luminance_widget = self.create_luminance_input()

        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.save_tolerances)

        self.layout.addWidget(self.ellipse1_widget)
        self.layout.addWidget(self.ellipse2_widget)
        self.layout.addWidget(self.rotation_widget)  # Add rotation widget
        self.layout.addWidget(self.luminance_widget)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

        self.load_values()

    def create_ellipse_inputs(self, title):
        ellipse_widget = QWidget()
        ellipse_layout = QVBoxLayout(ellipse_widget)

        ellipse_label = QLabel(title)
        ellipse_label.setProperty('bold', True)
        ellipse_layout.addWidget(ellipse_label)

        width_input = self.create_input_field('Width:')
        height_input = self.create_input_field('Height:')

        ellipse_layout.addLayout(width_input)
        ellipse_layout.addLayout(height_input)

        inputs = {
            "width": width_input,
            "height": height_input,
        }

        return ellipse_widget, inputs

    def create_input_field(self, label_text):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit(self)
        layout.addWidget(label)
        layout.addWidget(line_edit)
        return layout

    def create_luminance_input(self):
        luminance_widget = QWidget()
        layout = QVBoxLayout(luminance_widget)
        label = QLabel('Luminance:')
        label.setProperty('bold', True)
        self.luminance_line_edit = QLineEdit(self)
        layout.addWidget(label)
        layout.addWidget(self.luminance_line_edit)
        return luminance_widget

    def create_rotation_input(self):
        rotation_widget = QWidget()
        layout = QHBoxLayout(rotation_widget)
        label = QLabel('Rotation:')
        label.setProperty('bold', True)
        self.rotation_line_edit = QLineEdit(self)
        layout.addWidget(label)
        layout.addWidget(self.rotation_line_edit)
        return rotation_widget

    def load_values(self):
        if len(config.ellipse_characteristics) >= 5:
            width1, height1 = config.ellipse_characteristics[0], config.ellipse_characteristics[1]
            width2, height2 = config.ellipse_characteristics[2], config.ellipse_characteristics[3]
            rotation = config.ellipse_characteristics[4]

            self.ellipse1_inputs["width"].itemAt(1).widget().setText(str(width1))
            self.ellipse1_inputs["height"].itemAt(1).widget().setText(str(height1))
            self.ellipse2_inputs["width"].itemAt(1).widget().setText(str(width2))
            self.ellipse2_inputs["height"].itemAt(1).widget().setText(str(height2))
            self.rotation_line_edit.setText(str(rotation))

        if config.luminance:
            self.luminance_line_edit.setText(str(config.luminance[0]))

    def save_tolerances(self):
        config.ellipse_characteristics = [
            float(self.ellipse1_inputs["width"].itemAt(1).widget().text()),
            float(self.ellipse1_inputs["height"].itemAt(1).widget().text()),
            float(self.ellipse2_inputs["width"].itemAt(1).widget().text()),
            float(self.ellipse2_inputs["height"].itemAt(1).widget().text()),
            float(self.rotation_line_edit.text())
        ]
        config.luminance = [float(self.luminance_line_edit.text())]

        # Trigger updates in both plotters
        self.parent.xy_plotter.plot_sample_points()
        self.parent.main_window.color_variations_plotter.plot_sample_points()

        self.accept()
