from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import MySQLdb as db
from hashlib import md5
import pandas as pd

import os
import sys

# import util.ui_loader as ui_loader
from util import *
from models import *
# from util import ui_loader, db_connector, message_box, standardized, common
# from client.controllers.building_controller import *
# from client.util import ui_loader, db_connector, message_box, standardized, common
# import client.util.ui_loader as ui_loader
# from models import my_model
# from client.util import ui_loader

ui = ui_loader.load_ui('../resources/security.ui')


class MainSecurity(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.frame_main.setHidden(True)
        self.frame_login.setHidden(False)
        self.setWindowTitle("Face Access Control")
        self.database = db_connector.connector('localhost', 'henrydb', 'root', 'face_recognition')
        if self.database == None:
            msg = message_box.MyMessageBox(QMessageBox.Critical,"Wrong db or authentication", "You must change setting in .config file")
            sys.exit(msg.exec())
        self.load_data()
        self.handle_buttons()
        self.handle_ui()
        self.handle_combobox()
        self.combobox_setting()
        self.combobox_setting_data_change()
        self.handle_search_line_edit()
        self.session = 'NoOne'
        self.table_widget_setting()
        self.handle_ui_login()
        self.button_setting_and_ui()
        self.open_window()
        
        #for test ting
        self.handle_frame_ui()

    def check_login(self):
        print(self.session)
        if self.session == None:
            sys.exit()
        if self.session == 'NoOne':
            self.handle_frame_ui()

    def handle_ui(self):
        self.label_username_session.setStyleSheet("QLabel{font-family: ubuntu 30; color: blue; font-weight: bold}")
        self.tabWidget_main.tabBar().setVisible(False)
        self.tabWidget_access_control.tabBar().setVisible(False)

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

    #load_data
    def load_data(self):
        pass
        # self.load_building_manage()
        # self.load_apartment_manage()
        # self.load_resident_manage()
        # self.load_guest_manage()
        # self.load_access_control()
        
    def button_setting_and_ui(self):
        pass
        # self.building_manage_button_setting_and_ui()
        # self.apartment_manage_button_setting_and_ui()
        # self.resident_manage_button_setting_and_ui()
        # self.guest_manage_button_setting_and_ui()
        # self.access_control_button_setting_and_ui()

        
    def handle_buttons(self):
        # self.handle_buttons_login_tab()
        # self.handle_buttons_main_tab()
        # #handle button for bulding manage
        # self.building_manage_handle_button()
        # self.apartment_manage_handle_button()
        # self.resident_manage_handle_button()
        # self.guest_manage_handle_button()
        pass

    def handle_buttons_main_tab(self):
        pass
        # self.pushButton_buiding_manage.clicked.connect(self.open_tab_building)
        # self.pushButton_apartment_manage.clicked.connect(self.open_tab_apartment)
        # self.pushButton_resident_manage.clicked.connect(self.open_tab_resident)
        # self.pushButton_gest_manage.clicked.connect(self.open_tab_guest)
        # self.pushButton_video_access_control.clicked.connect(self.open_tab_access_control)

    def handle_buttons_login_tab(self):
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_logout.clicked.connect(self.logout)
        self.lineEdit_password.returnPressed.connect(self.login)

    def handle_combobox(self):
        pass
        # handle action for combobox in buiding manage tab
        # self.guest_manage_handle_combobox()
        # self.access_control_handle_combobox()

    def combobox_setting(self):
        pass
        # setting combobox data for satatic combobox
        # self.guest_manage_combobox_setting()
        # self.access_control_combobox_setting()

    def combobox_setting_data_change(self):
        pass
        # self.guest_manage_combobox_setting_data_change()
        # self.access_control_combobox_setting_data_change()

    # table widget setting
    def table_widget_setting(self):
        pass
        # self.guest_manage_table_widget_setting()
        # self.access_control_table_widget_setting()

    def handle_search_line_edit(self):
        pass
        # handle line edit using for search
        # self.guest_manage_handle_search_line_edit()
        # self.access_control_handle_search_line_edit()

    def login(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        cursor = self.database.cursor()
        cursor.execute("select * from user where username='{}' and password='{}'".format(username, md5(password.encode()).hexdigest()))
        for i in range(cursor.rowcount):
            result = cursor.fetchall()
            if len(result) == 1:
                self.session = username
                cursor.close()
                break
        if self.session:
            self.label_username_session.setText(self.session)
            self.handle_frame_ui()
            self.lineEdit_username.setText('')
            self.lineEdit_password.setText('')
            self.label_error.setText('')
            self.load_data()
        else:
            self.label_error.setText('Wrong username or password')
    
    def logout(self):
        self.session = None
        self.handle_frame_ui()
        # To do: set all line, textedit to ''

    # open tab main

    # default init window
    def open_window(self):
        #for testing
        #self.check_login()
        # self.open_tab_building()
        pass

    def open_tab_guest(self):
        pass
        # self.tabWidget_main.setCurrentIndex(3)

        # common.set_tab_when_clicked(self.pushButton_gest_manage,
        #  self.pushButton_buiding_manage, self.pushButton_apartment_manage,
        #  self.pushButton_resident_manage, self.pushButton_gest_manage,
        #  self.pushButton_video_access_control)

    def open_tab_access_control(self):
        pass
        # self.tabWidget_main.setCurrentIndex(4)

        # common.set_tab_when_clicked(self.pushButton_video_access_control,
        #  self.pushButton_buiding_manage, self.pushButton_apartment_manage,
        #  self.pushButton_resident_manage, self.pushButton_gest_manage,
        #  self.pushButton_video_access_control)