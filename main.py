# main.py

import sys
from PyQt5.QtWidgets import QApplication
from ui.CustomWindow import CustomWindow

def main():
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
