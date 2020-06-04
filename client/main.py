from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from PyQt5.uic import loadUiType
ui,_ = loadUiType('./main.ui')

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

def main():
    app = QApplication([])
    window = MainApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()