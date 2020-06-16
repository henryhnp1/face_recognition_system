from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb as db
from util import ui_loader, db_connector, message_box, file_reader
from hashlib import md5


ui = ui_loader.load_ui('../resources/main.ui')


class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.frame_main.setHidden(True)
        self.frame_login.setHidden(False)
        self.setWindowTitle("Face Access Control")
        self.handle_ui_login()
        self.handle_buttons()
        self.handle_ui()
        self.session = None

    def handle_ui(self):
        self.label_username_session.setStyleSheet("QLabel{font-family: ubuntu 30; color: blue; font-weight: bold}")
        self.tabWidget_main.tabBar().setVisible(False)
        self.tabWidget_building_manage.tabBar().setVisible(False)

    def handle_buttons(self):
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_logout.clicked.connect(self.logout)
        self.lineEdit_password.returnPressed.connect(self.login)

        # handle button for main manager
        self.pushButton_buiding_manager.clicked.connect(self.open_tab_building)
        self.pushButton_apartment_manager.clicked.connect(self.open_tab_apartment)
        self.pushButton_resident_manager.clicked.connect(self.open_tab_resident)
        self.pushButton_gest_manager.clicked.connect(self.open_tab_guest)
        self.pushButton_video_access_control.clicked.connect(self.open_tab_access_control)

        #handle button for bulding manager
        self.pushButton_block_manage.clicked.connect(self.open_tab_block)
        self.pushButton_floor_manage.clicked.connect(self.open_tab_floor)
        self.pushButton_door_manage.clicked.connect(self.open_tab_door)
        self.pushButton_setting_manage.clicked.connect(self.open_tab_setting)


    def handle_frame_ui(self):
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
        con = db_connector.connector('localhost', 'henrydb', 'root', 'face_recognition')
        if con == None:
            msg = message_box.MyMessageBox(QMessageBox.Critical,"Wrong db or authentication", "You must change setting in .config file").exec()
        else:
            cursor = con.cursor()
            cursor.execute("select * from user where username='{}' and password='{}'".format(username, md5(password.encode()).hexdigest()))
            for i in range(cursor.rowcount):
                result = cursor.fetchall()
                if len(result) == 1:
                    self.session = username
                    break
            if self.session:
                self.label_username_session.setText(self.session)
                self.handle_frame_ui()
                self.lineEdit_username.setText('')
                self.lineEdit_password.setText('')
            else:
                self.label_error.setText('Wrong username or password')
    
    def logout(self):
        self.session = None
        self.handle_frame_ui()

    def open_tab_building(self):
        self.tabWidget_main.setCurrentIndex(0)

    def open_tab_apartment(self):
        self.tabWidget_main.setCurrentIndex(1)

    def open_tab_resident(self):
        self.tabWidget_main.setCurrentIndex(2)

    def open_tab_guest(self):
        self.tabWidget_main.setCurrentIndex(3)

    def open_tab_access_control(self):
        self.tabWidget_main.setCurrentIndex(4)

    def open_tab_block(self):
        self.tabWidget_building_manage.setCurrentIndex(0)
    
    def open_tab_floor(self):
        self.tabWidget_building_manage.setCurrentIndex(1)

    def open_tab_door(self):
        self.tabWidget_building_manage.setCurrentIndex(2)

    def open_tab_setting(self):
        self.tabWidget_building_manage.setCurrentIndex(3)
        

def main():
    app = QApplication([])
    window = MainApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
