from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb as db
from util import ui_loader


ui = ui_loader.load_ui('./resources/main.ui')


class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.frame_main.setHidden(True)
        self.frame_login.setHidden(False)
        
        self.pushButton_login.clicked.connect(self.login)
        self.lineEdit_password.returnPressed.connect(self.login)
        self.lineEdit_username.returnPressed.connect(self.pushButton_login.clicked)

        self.handle_ui_login()

    def handle_ui(self):
        self.frame_main.setHidden(not self.frame_main.isHidden())
        self.frame_login.setHidden(not self.frame_login.isHidden())
    
    def handle_ui_login(self):
        self.label_login.setStyleSheet("QLabel{font-family: ubuntu 30; color: blue}")
        self.label_error.setText('')
        self.label_error.setStyleSheet("QLabel{font-family: ubuntu 14; color: red}")
        self.lineEdit_username.setStyleSheet("QLineEdit{border: 1px solid gray; border-radius:10px;}")
        self.lineEdit_password.setStyleSheet("QLineEdit{border: 1px solid gray; border-radius:10px;}")
        self.pushButton_login.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px;"
                                            " background-color: green; color:white}")

    def login(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        print(password, username)
        

def main():
    app = QApplication([])
    window = MainApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
