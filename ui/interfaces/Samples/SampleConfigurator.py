# ui/interfaces/Samples/SampleConfigurator.py

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class SampleConfigurator(QDialog):
    def __init__(self, parent=None):
        super(SampleConfigurator, self).__init__(parent)
        self.setWindowTitle('Add Sample')
        self.setGeometry(100, 100, 300, 200)

        self.setStyleSheet("""
            QLabel {
                color: white;
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

        self.name_layout = self.create_input_field('Name:')
        self.x_layout = self.create_input_field('x:')
        self.y_layout = self.create_input_field('y:')
        self.Y_layout = self.create_input_field('Y:')

        self.save_button = QPushButton('Add Sample', self)
        self.save_button.clicked.connect(self.accept)

        self.layout.addLayout(self.name_layout)
        self.layout.addLayout(self.x_layout)
        self.layout.addLayout(self.y_layout)
        self.layout.addLayout(self.Y_layout)
        self.layout.addWidget(self.save_button)
        self.setLayout(self.layout)

    def create_input_field(self, label_text):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit(self)
        layout.addWidget(label)
        layout.addWidget(line_edit)
        return layout

    def get_sample_data(self):
        name = self.name_layout.itemAt(1).widget().text()
        x = float(self.x_layout.itemAt(1).widget().text())
        y = float(self.y_layout.itemAt(1).widget().text())
        Y = float(self.Y_layout.itemAt(1).widget().text())
        return name, x, y, Y
