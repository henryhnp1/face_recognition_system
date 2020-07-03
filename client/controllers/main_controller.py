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

ui = ui_loader.load_ui('../resources/main.ui')


class MainApp(QMainWindow, ui):

    from controllers.building.building_controller import load_building_manage
    from controllers.building.building_controller import open_tab_block, open_tab_floor, open_tab_door, open_tab_setting
    from controllers.building.building_controller import building_manage_button_setting_and_ui, building_manage_handle_combobox, building_manage_table_widget_setting
    from controllers.building.building_controller import building_manage_combobox_setting, building_manage_combobox_setting_data_change, building_manage_handle_search_line_edit, building_manage_handle_button

    from controllers.building.setting_tab import building_manage_setting_load, load_permission_setting, load_type_of_floor_setting
    from controllers.building.setting_tab import building_manage_handle_button_setting_tab, building_manage_handle_button_setting_tab_permission_table, building_manage_handle_button_setting_tab_type_of_floor_table, building_manage_handle_combobox_setting_tab, building_manage_handle_search_line_edit_setting_tab
    from controllers.building.setting_tab import building_manage_button_setting_and_ui_setting_tab, building_manage_combobox_setting_data_change_setting_tab
    from controllers.building.setting_tab import building_manage_combobox_setting_setting_tab, building_manage_setting_tab_table_widget_setting
    from controllers.building.setting_tab import add_type_of_floor, edit_type_of_floor, delete_type_of_floor, select_file_type_of_floor, search_type_of_floor, set_line_search_type_of_building, import_type_of_floor, type_of_floor_click
    from controllers.building.setting_tab import add_permission, edit_permission, delete_permission, search_permission, select_file_permission, set_line_search_permission, import_permission, permission_click

    from controllers.building.block_tab import building_manage_block_manage_load
    from controllers.building.block_tab import building_manage_button_setting_and_ui_block_tab, building_manage_combobox_setting_block_manage_tab, building_manage_combobox_setting_data_change_block_manage_tab
    from controllers.building.block_tab import building_manage_block_manage_setting_blank_form, building_manage_block_manage_setting_line_search, building_manage_block_manage_tab_table_widget_setting
    from controllers.building.block_tab import building_manage_handle_button_block_manage_tab, building_manage_handle_combobox_block_manage_tab, building_manage_handle_search_line_edit_block_tab
    from controllers.building.block_tab import building_manage_block_manage_add_block, building_manage_block_manage_edit_block, building_manage_block_manage_delete_block
    from controllers.building.block_tab import building_manage_block_manage_search_block, building_manage_block_manage_block_item_click

    from controllers.building.floor_tab import building_manage_floor_manage_load, building_manage_floor_manage_tab_table_widget_setting, building_manage_floor_manage_clear_form
    from controllers.building.floor_tab import building_manage_floor_manage_setting_line_search, building_manage_button_setting_and_ui_floor_tab, building_manage_combobox_setting_data_change_floor_manage_tab, building_manage_combobox_setting_floor_manage_tab
    from controllers.building.floor_tab import building_manage_floor_manage_select_file_import_floor, building_manage_floor_manage_floor_item_click, building_manage_floor_manage_import_file_floor
    from controllers.building.floor_tab import building_manage_handle_button_floor_manage_tab, building_manage_handle_combobox_floor_manage_tab, building_manage_handle_search_line_edit_floor_tab
    from controllers.building.floor_tab import building_manage_floor_manage_add_floor, building_manage_floor_manage_edit_floor, building_manage_floor_manage_delete_floor, building_manage_floor_manage_search_floor
    
    from controllers.building.door_tab import building_manage_door_manage_load, building_manage_combobox_setting_data_change_door_manage_tab_building_combobox
    from controllers.building.door_tab import building_manage_button_setting_and_ui_door_tab, building_manage_combobox_setting_data_change_door_manage_tab, building_manage_combobox_setting_door_manage_tab
    from controllers.building.door_tab import building_manage_door_manage_tab_table_widget_setting, building_manage_handle_button_door_manage_tab, building_manage_handle_combobox_door_manage_tab, building_manage_handle_search_line_edit_door_tab
    from controllers.building.door_tab import building_manage_door_manage_search_door, building_manage_door_manage_door_table_load, building_manage_door_manage_role_door_table_load
    from controllers.building.door_tab import building_manage_door_manage_role_door_item_click, building_manage_door_manage_door_item_click, building_manage_combobox_setting_data_change_door_manage_tab_role_door_combobox, building_manage_combobox_setting_data_change_door_manage_tab_floor_combobox

    from controllers.apartment.apartment_controller import apartment_manage_button_setting_and_ui, apartment_manage_combobox_setting, apartment_manage_combobox_setting_data_change, apartment_manage_table_widget_setting
    from controllers.apartment.apartment_controller import apartment_manage_handle_button, apartment_manage_handle_combobox, apartment_manage_handle_search_line_edit
    from controllers.apartment.apartment_controller import load_apartment_manage

    from controllers.resident.resident_controller import load_resident_manage, resident_manage_table_widget_setting
    from controllers.resident.resident_controller import resident_manage_button_setting_and_ui, resident_manage_combobox_setting, resident_manage_combobox_setting_data_change
    from controllers.resident.resident_controller import resident_manage_handle_button, resident_manage_handle_combobox, resident_manage_handle_search_line_edit

    from controllers.guest.guest_controller import load_guest_manage, guest_manage_table_widget_setting
    from controllers.guest.guest_controller import guest_manage_button_setting_and_ui, guest_manage_combobox_setting, guest_manage_combobox_setting_data_change
    from controllers.guest.guest_controller import guest_manage_handle_button, guest_manage_handle_combobox, guest_manage_handle_search_line_edit

    from controllers.access_control.access_control_controller import load_access_control, access_control_table_widget_setting
    from controllers.access_control.access_control_controller import access_control_button_setting_and_ui, access_control_combobox_setting, access_control_combobox_setting_data_change
    from controllers.access_control.access_control_controller import access_control_handle_button, access_control_handle_combobox, access_control_handle_search_line_edit

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
        self.tabWidget_building_manage.tabBar().setVisible(False)

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
        self.load_building_manage()
        self.load_apartment_manage()
        self.load_resident_manage()
        self.load_guest_manage()
        self.load_access_control()
        
    def button_setting_and_ui(self):
        self.building_manage_button_setting_and_ui()
        self.apartment_manage_button_setting_and_ui()
        self.resident_manage_button_setting_and_ui()
        self.guest_manage_button_setting_and_ui()
        self.access_control_button_setting_and_ui()

        
    def handle_buttons(self):
        self.handle_buttons_login_tab()
        self.handle_buttons_main_tab()
        #handle button for bulding manage
        self.building_manage_handle_button()
        self.apartment_manage_handle_button()
        self.resident_manage_handle_button()
        self.guest_manage_handle_button()

    def handle_buttons_main_tab(self):
        self.pushButton_buiding_manage.clicked.connect(self.open_tab_building)
        self.pushButton_apartment_manage.clicked.connect(self.open_tab_apartment)
        self.pushButton_resident_manage.clicked.connect(self.open_tab_resident)
        self.pushButton_gest_manage.clicked.connect(self.open_tab_guest)
        self.pushButton_video_access_control.clicked.connect(self.open_tab_access_control)

    def handle_buttons_login_tab(self):
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_logout.clicked.connect(self.logout)
        self.lineEdit_password.returnPressed.connect(self.login)

    def handle_combobox(self):
        # handle action for combobox in buiding manage tab
        self.building_manage_handle_combobox()
        self.apartment_manage_handle_combobox()
        self.resident_manage_handle_combobox()
        self.guest_manage_handle_combobox()
        self.access_control_handle_combobox()

    def combobox_setting(self):
        # setting combobox data for satatic combobox
        # setting for building manage tab
        self.building_manage_combobox_setting()
        self.apartment_manage_combobox_setting()
        self.resident_manage_combobox_setting()
        self.guest_manage_combobox_setting()
        self.access_control_combobox_setting()

    def combobox_setting_data_change(self):
        self.building_manage_combobox_setting_data_change()
        self.apartment_manage_combobox_setting_data_change()
        self.resident_manage_combobox_setting_data_change()
        self.guest_manage_combobox_setting_data_change()
        self.access_control_combobox_setting_data_change()

    # table widget setting
    def table_widget_setting(self):
        self.building_manage_table_widget_setting()
        self.apartment_manage_table_widget_setting()
        self.resident_manage_table_widget_setting()
        self.guest_manage_table_widget_setting()
        self.access_control_table_widget_setting()

    def handle_search_line_edit(self):
        # handle line edit using for search
        # handle search line edit for building manage tab
        self.building_manage_handle_search_line_edit()
        self.apartment_manage_handle_search_line_edit()
        self.resident_manage_handle_search_line_edit()
        self.guest_manage_handle_search_line_edit()
        self.access_control_handle_search_line_edit()

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
        self.open_tab_building()

    def open_tab_building(self):
        #for testing
        #self.check_login()

        self.tabWidget_main.setCurrentIndex(0)

        common.set_tab_when_clicked(self.pushButton_buiding_manage,
         self.pushButton_buiding_manage, self.pushButton_apartment_manage,
         self.pushButton_resident_manage, self.pushButton_gest_manage,
         self.pushButton_video_access_control)
        
        # setting current tab when the window first load
        self.tabWidget_building_manage.setCurrentIndex(0)
        common.set_tab_when_clicked(self.pushButton_block_manage, self.pushButton_floor_manage,
         self.pushButton_door_manage, self.pushButton_setting_manage)

    def open_tab_apartment(self):
        self.tabWidget_main.setCurrentIndex(1)

        common.set_tab_when_clicked(self.pushButton_apartment_manage,
         self.pushButton_buiding_manage, self.pushButton_apartment_manage,
         self.pushButton_resident_manage, self.pushButton_gest_manage,
         self.pushButton_video_access_control)

    def open_tab_resident(self):
        self.tabWidget_main.setCurrentIndex(2)

        common.set_tab_when_clicked(self.pushButton_resident_manage,
         self.pushButton_buiding_manage, self.pushButton_apartment_manage,
         self.pushButton_resident_manage, self.pushButton_gest_manage,
         self.pushButton_video_access_control)

    def open_tab_guest(self):
        self.tabWidget_main.setCurrentIndex(3)

        common.set_tab_when_clicked(self.pushButton_gest_manage,
         self.pushButton_buiding_manage, self.pushButton_apartment_manage,
         self.pushButton_resident_manage, self.pushButton_gest_manage,
         self.pushButton_video_access_control)

    def open_tab_access_control(self):
        self.tabWidget_main.setCurrentIndex(4)

        common.set_tab_when_clicked(self.pushButton_video_access_control,
         self.pushButton_buiding_manage, self.pushButton_apartment_manage,
         self.pushButton_resident_manage, self.pushButton_gest_manage,
         self.pushButton_video_access_control)
