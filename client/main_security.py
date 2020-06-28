from PyQt5.QtWidgets import *
import sys
from controllers.main_security_controller import MainSecurity


def main():
    app = QApplication([])
    window = MainSecurity()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()