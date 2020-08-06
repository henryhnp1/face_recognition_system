from PyQt5.QtWidgets import *
import sys
from controllers.main_controller import MainApp

def main():
    app = QApplication([])
    window = MainApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()