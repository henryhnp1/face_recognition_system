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

    from controllers.building.building_controller import load_building_manage, admin_building_clear_form
    from controllers.building.building_controller import open_tab_block, open_tab_floor, open_tab_door, open_tab_setting
    from controllers.building.building_controller import building_manage_button_setting_and_ui, building_manage_handle_combobox, building_manage_table_widget_setting
    from controllers.building.building_controller import building_manage_combobox_setting, building_manage_combobox_setting_data_change, building_manage_handle_search_line_edit, building_manage_handle_button

    from controllers.building.setting_tab import building_manage_setting_load, load_permission_setting, load_type_of_floor_setting, admin_building_setting_clear_form, admin_building_setting_permission_clear_form, admin_building_setting_type_of_floor_clear_form
    from controllers.building.setting_tab import building_manage_handle_button_setting_tab, building_manage_handle_button_setting_tab_permission_table, building_manage_handle_button_setting_tab_type_of_floor_table, building_manage_handle_combobox_setting_tab, building_manage_handle_search_line_edit_setting_tab
    from controllers.building.setting_tab import building_manage_button_setting_and_ui_setting_tab, building_manage_combobox_setting_data_change_setting_tab
    from controllers.building.setting_tab import building_manage_combobox_setting_setting_tab, building_manage_setting_tab_table_widget_setting
    from controllers.building.setting_tab import add_type_of_floor, edit_type_of_floor, delete_type_of_floor, select_file_type_of_floor, search_type_of_floor, set_line_search_type_of_building, import_type_of_floor, type_of_floor_click
    from controllers.building.setting_tab import add_permission, edit_permission, delete_permission, search_permission, select_file_permission, set_line_search_permission, import_permission, permission_click

    from controllers.building.block_tab import building_manage_block_manage_load, admin_building_block_clear_form
    from controllers.building.block_tab import building_manage_button_setting_and_ui_block_tab, building_manage_combobox_setting_block_manage_tab, building_manage_combobox_setting_data_change_block_manage_tab
    from controllers.building.block_tab import building_manage_block_manage_setting_blank_form, building_manage_block_manage_setting_line_search, building_manage_block_manage_tab_table_widget_setting
    from controllers.building.block_tab import building_manage_handle_button_block_manage_tab, building_manage_handle_combobox_block_manage_tab, building_manage_handle_search_line_edit_block_tab
    from controllers.building.block_tab import building_manage_block_manage_add_block, building_manage_block_manage_edit_block, building_manage_block_manage_delete_block
    from controllers.building.block_tab import building_manage_block_manage_search_block, building_manage_block_manage_block_item_click

    from controllers.building.floor_tab import building_manage_floor_manage_load, building_manage_floor_manage_tab_table_widget_setting, building_manage_floor_manage_clear_form, admin_building_floor_clear_form
    from controllers.building.floor_tab import building_manage_floor_manage_setting_line_search, building_manage_button_setting_and_ui_floor_tab, building_manage_combobox_setting_data_change_floor_manage_tab, building_manage_combobox_setting_floor_manage_tab
    from controllers.building.floor_tab import building_manage_floor_manage_select_file_import_floor, building_manage_floor_manage_floor_item_click, building_manage_floor_manage_import_file_floor
    from controllers.building.floor_tab import building_manage_handle_button_floor_manage_tab, building_manage_handle_combobox_floor_manage_tab, building_manage_handle_search_line_edit_floor_tab
    from controllers.building.floor_tab import building_manage_floor_manage_add_floor, building_manage_floor_manage_edit_floor, building_manage_floor_manage_delete_floor, building_manage_floor_manage_search_floor
    
    from controllers.building.door_tab import building_manage_door_manage_load, building_manage_combobox_setting_data_change_door_manage_tab_building_combobox, admin_building_door_clear_form
    from controllers.building.door_tab import building_manage_button_setting_and_ui_door_tab, building_manage_combobox_setting_data_change_door_manage_tab, building_manage_combobox_setting_door_manage_tab
    from controllers.building.door_tab import building_manage_door_manage_tab_table_widget_setting, building_manage_handle_button_door_manage_tab, building_manage_handle_combobox_door_manage_tab, building_manage_handle_search_line_edit_door_tab, building_manage_door_manage_clear_role_door_form
    from controllers.building.door_tab import building_manage_door_manage_search_door, building_manage_door_manage_door_table_load, building_manage_door_manage_role_door_table_load, building_manage_seach_line_edit_setting_search_role_door, building_manage_seach_line_edit_setting_search_door
    from controllers.building.door_tab import building_manage_door_manage_role_door_item_click, building_manage_door_manage_door_item_click, building_manage_combobox_setting_data_change_door_manage_tab_role_door_combobox, building_manage_combobox_setting_data_change_door_manage_tab_floor_combobox
    from controllers.building.door_tab import building_manage_door_manage_search_door, building_manage_door_manage_search_role_door, building_manage_door_manage_add_door, building_manage_door_manage_add_role_door, building_manage_door_manage_edit_door, building_manage_door_manage_edit_role_door
    from controllers.building.door_tab import building_manage_door_manage_delete_door, building_manage_door_manage_delete_role_door, building_manage_door_manage_choose_file_door_import, building_manage_door_manage_import_file_door, building_manage_door_mange_export_file_door, building_manage_door_manage_clear_door_form

    from controllers.apartment.apartment_controller import apartment_manage_button_setting_and_ui, apartment_manage_combobox_setting, apartment_manage_combobox_setting_data_change, apartment_manage_table_widget_setting
    from controllers.apartment.apartment_controller import apartment_manage_handle_button, apartment_manage_handle_combobox, apartment_manage_handle_search_line_edit
    from controllers.apartment.apartment_controller import load_apartment_manage, apartment_manage_open_tab_company, apartment_manage_open_tab_apartment, admin_apartment_clear_form

    from controllers.apartment.apartment_tab import apartment_manage_load_apartment_tab, apartment_manage_handle_combobox_apartment_tab, apartment_manage_handle_combobox_apartment_tab, apartment_manage_combobox_setting_apartment_tab, apartment_manage_combobox_setting_data_change_apartment_tab, apartment_manage_resident_mange_handle_spinbox, apartment_manage_resident_manage_setting_prefix_apartment
    from controllers.apartment.apartment_tab import apartment_manage_handle_search_line_edit_apartment_tab, apartment_manage_table_widget_setting_apartment_tab, apartment_manage_button_setting_and_ui_apartment_tab, apartment_manage_handle_button_apartment_tab, apartment_manage_setting_data_change_prefix_apartment, apartment_manage_setting_data_change_floor_combobox, apartment_manage_apartment_item_click
    from controllers.apartment.apartment_tab import apartment_manage_apartment_setting_line_search, apartment_manage_search_apartment, apartment_manage_export_apartment, apartment_manage_select_import_apartment, apartment_manage_import_apartment, apartment_manage_add_apartment, apartment_manage_edit_apartment, apartment_manage_delete_apartment, apartment_manage_clear_apartment_form, admin_apartment_apartment_clear_form

    from controllers.apartment.company_tab import apartment_manage_load_company_tab, apartment_manage_handle_combobox_company_tab, apartment_manage_combobox_setting_company_tab, apartment_manage_combobox_setting_data_change_company_tab, apartment_manage_combobox_setting_company_tab, apartment_manage_clear_data_form_company_form, apartment_manage_clear_data_form_office_form
    from controllers.apartment.company_tab import apartment_manage_handle_search_line_edit_company_tab, apartment_manage_table_widget_setting_company_tab, apartment_manage_button_setting_and_ui_company_tab, apartment_manage_combobox_setting_company_tab, apartment_manage_load_company_tab_load_office_table, apartment_manage_load_company_tab_load_company_table, admin_apartment_company_clear_form, admin_apartment_company_office_clear_form
    from controllers.apartment.company_tab import apartment_manage_combobox_setting_data_change_company_tab_office_table, apartment_manage_combobox_setting_data_change_company_tab_office_table_block_combobox, apartment_manage_combobox_setting_data_change_company_tab_office_table_floor_combobox, apartment_manage_combobox_setting_data_change_company_tab_company_table
    from controllers.apartment.company_tab import apartment_manage_search_line_edit_setting_search_office, apartment_manage_search_line_edit_setting_search_company, apartment_manage_search_office, apartment_manage_search_company, apartment_manage_office_item_click, apartment_manage_company_item_click, apartment_manage_delete_company, apartment_manage_select_import_company, apartment_manage_import_company
    from controllers.apartment.company_tab import apartment_manage_set_prefix_office_number, apartment_manage_clear_data_form_company_form, apartment_manage_add_office, apartment_manage_edit_office, apartment_manage_delete_office, apartment_manage_select_file_import_office, apartment_manage_import_office, apartment_manage_add_company, apartment_manage_edit_company
    from controllers.apartment.company_tab import apartment_manage_handle_button_company_tab_office_table, apartment_manage_handle_button_company_tab_company_table, apartment_manage_handle_button_company_tab, apartment_manage_export_company, apartment_manage_export_office, apartment_manage_combobox_setting_data_change_company_tab_floor_combobox, apartment_manage_combobox_setting_data_change_company_tab_office_combobox

    from controllers.resident.resident_controller import load_resident_manage, resident_manage_table_widget_setting, admin_resident_clear_form
    from controllers.resident.resident_controller import resident_manage_button_setting_and_ui, resident_manage_combobox_setting, resident_manage_combobox_setting_data_change
    from controllers.resident.resident_controller import resident_manage_handle_button, resident_manage_handle_combobox, resident_manage_handle_search_line_edit, resident_manage_open_tab_resident, resident_manage_open_tab_staff

    from controllers.resident.staff_tab import resident_manage_staff_load, resident_manage_handle_button_staff_tab, resident_manage_handle_combobox_staff_tab, resident_manage_combobox_setting_staff_tab, resident_manage_combobox_setting_data_change_staff_tab, resident_manage_handle_search_line_edit_staff_tab, resident_manage_table_widget_setting_staff_tab, resident_manage_button_setting_and_ui_staff_tab
    from controllers.resident.staff_tab import resident_manage_staff_tab_setting_line_search, resident_manage_staff_tab_search_staff, resident_manage_staff_tab_add_staff, resident_manage_staff_tab_edit_staff, resident_manage_staff_tab_delete_staff, resident_manage_staff_tab_clear_form, resident_manage_staff_tab_select_file_import_staff, resident_manage_staff_tab_import_file_staff
    from controllers.resident.staff_tab import resident_manage_staff_tab_export_file_staff, resident_manage_staff_tab_item_click, resident_manage_staff_tab_data_change_floor_combobox, resident_manage_staff_tab_data_change_building_combobox, resident_manage_staff_tab_data_change_company_combobox

    from controllers.resident.resident_tab import resident_manage_resident_load, resident_manage_handle_button_resident_tab, resident_manage_handle_combobox_resident_tab, resident_manage_combobox_setting_resident_tab, resident_manage_combobox_setting_data_change_resident_tab, resident_manage_handle_search_line_edit_resident_tab, resident_manage_table_widget_setting_resident_tab
    from controllers.resident.resident_tab import resident_manage_button_setting_and_ui_resident_tab, resident_manage_resident_tab_setting_line_search, resident_manage_resident_tab_search_resident, resident_manage_resident_tab_add_resident, resident_manage_resident_tab_edit_resident, resident_manage_resident_tab_delete_resident, resident_manage_resident_tab_clear_form, resident_manage_resident_tab_data_change_building_combobox
    from controllers.resident.resident_tab import resident_manage_resident_tab_select_file_import_resident, resident_manage_resident_tab_import_file_resident, resident_manage_resident_tab_export_file_resident, resident_manage_resident_tab_item_click, resident_manage_resident_tab_data_change_floor_combobox,resident_manage_resident_tab_data_change_apartment_combobox

    from controllers.guest.guest_controller import load_guest_manage, guest_manage_table_widget_setting, admin_guest_clear_form
    from controllers.guest.guest_controller import guest_manage_button_setting_and_ui, guest_manage_combobox_setting, guest_manage_combobox_setting_data_change
    from controllers.guest.guest_controller import guest_manage_handle_button, guest_manage_handle_combobox, guest_manage_handle_search_line_edit

    from controllers.access_control.access_control_controller import load_access_control, access_control_table_widget_setting, access_control_handle_button, admin_access_control_clear_form
    from controllers.access_control.access_control_controller import access_control_button_setting_and_ui, access_control_combobox_setting, access_control_combobox_setting_data_change
    from controllers.access_control.access_control_controller import access_control_handle_combobox, access_control_handle_search_line_edit, access_control_open_tab_grant_role, access_control_open_tab_person_image, access_control_open_tab_access_track

    from controllers.access_control.grant_role_tab import access_control_grant_role_load, access_control_button_setting_and_ui_grant_role_tab, access_control_combobox_setting_data_change_grant_role_tab, access_control_combobox_setting_grant_role_tab, access_control_handle_button_grant_role_tab, access_control_handle_combobox_grant_role_tab, access_control_handle_search_line_edit_grant_role_tab, access_control_table_widget_setting_grant_role_tab, admin_access_control_grant_role_clear_form
    from controllers.access_control.grant_role_tab import access_control_button_setting_and_ui_grant_role_tab, access_control_grant_role_setting_line_search, access_control_grant_role_seach, access_control_grant_role_item_click, access_control_grant_role_export, access_control_grant_role_choose_file,  access_control_grant_role_import_file ,access_control_grant_role_add ,access_control_grant_role_edit ,access_control_grant_role_delete, access_control_grant_role_combobox_data_change_permission
    from controllers.access_control.grant_role_tab import access_control_grant_role_combobox_data_change_building_search ,access_control_grant_role_combobox_data_change_floor_search ,access_control_grant_role_combobox_data_change_door_search ,access_control_grant_role_combobox_data_change_building ,access_control_grant_role_combobox_data_change_floor ,access_control_grant_role_combobox_data_change_door, access_control_grant_role_setting_form

    from controllers.access_control.person_image_tab import access_control_person_image_load, access_control_button_setting_and_ui_person_image_tab, access_control_combobox_setting_data_change_person_image_tab, access_control_combobox_setting_person_image_tab, access_control_handle_button_person_image_tab, access_control_handle_combobox_person_image_tab, access_control_handle_search_line_edit_person_image_tab, access_control_table_widget_setting_person_image_tab, admin_access_control_person_image_clear_form
    from controllers.access_control.person_image_tab import access_control_person_image_load_person_table, access_control_person_image_setting_line_search, access_control_person_image_open_tab_add_photo, access_control_person_image_item_click, access_control_person_image_load_image_not_delete, access_control_person_image_load_image_delete, access_control_person_image_open_tab_manage_photo, access_control_person_image_delete_image, access_control_person_image_change_image_to_delete
    from controllers.access_control.person_image_tab import access_control_person_image_image_delete_click, access_control_person_image_image_not_delete_click, access_control_person_image_item_image_click, access_control_person_image_restore_image, on_pushButton_capture_image_admin_clicked, access_control_person_image_setting_button_capture, on_pushButton_start_cam_admin_clicked, access_control_person_image_stop_camera_capture, access_control_person_image_clear_form_and_ui
    from controllers.access_control.person_image_tab import access_control_person_image_add_image_capture, access_control_person_image_delete_image_capture, access_control_person_image_image_capture_click, access_control_person_image_select_folder_image, access_control_person_image_import_folder_image, access_control_person_image_search

    from controllers.access_control.access_track_tab import access_control_access_track_load, access_control_button_setting_and_ui_access_track_tab, access_control_combobox_setting_data_change_access_track_tab, access_control_combobox_setting_access_track_tab, access_control_handle_button_access_track_tab, access_control_handle_combobox_access_track_tab, access_control_handle_search_line_edit_access_track_tab, access_control_table_widget_setting_access_track_tab, admin_acesss_control_access_track_clear_form

    from controllers.security_guest.security_guest_controller import security_guest_clear_form, load_security_guest, security_guest_handle_button, security_guest_handle_combobox, security_guest_combobox_setting, security_guest_combobox_setting_data_change, security_guest_handle_search_line_edit, security_guest_table_widget_setting, security_guest_button_setting_and_ui, security_guest_open_tab_guest_visit,security_guest_open_tab_guest_image
    from controllers.security_guest.security_guest_visit_tab import security_guest_guest_visit_clear_form, security_guest_guest_visit_load, security_guest_handle_button_guest_visit_tab, security_guest_handle_combobox_guest_visit_tab, security_guest_combobox_setting_guest_visit_tab,security_guest_combobox_setting_data_change_guest_visit_tab, security_guest_handle_search_line_edit_guest_visit_tab, security_guest_table_widget_setting_guest_visit_tab, security_guest_button_setting_and_ui_guest_visit_tab
    from controllers.security_guest.security_guest_visit_tab import security_guest_guest_visit_tab_setting_line_search, security_guest_guest_visit_item_click, security_guest_guest_visit_search, security_guest_guest_visit_setting_target_visit, security_guest_guest_visit_export_guest_visit, security_guest_guest_visit_add_guest_visit, security_guest_guest_visit_edit_guest_visit, security_guest_guest_visit_delete_guest_visit
    from controllers.security_guest.security_guest_visit_tab import security_guest_visit_bussiness_data_change_building_combobox, security_guest_visit_resident_data_change_building_combobox, security_guest_visit_bussiness_data_change_floor_combobox, security_guest_visit_resident_data_change_floor_combobox, security_guest_visit_bussiness_data_change_company_combobox, security_guest_visit_resident_data_change_apartment_combobox

    from controllers.security_guest.security_guest_image_tab import security_guest_image_clear_form, security_guest_image_load, security_guest_image_handle_button_guest_image_tab, security_guest_image_handle_combobox_guest_image_tab, security_guest_image_combobox_setting_guest_image_tab, security_guest_image_combobox_setting_data_change_guest_image_tab, security_guest_image_handle_search_line_edit_guest_image_tab, security_guest_image_table_widget_setting_guest_image_tab, security_guest_image_import_folder_image
    from controllers.security_guest.security_guest_image_tab import security_guest_image_button_setting_and_ui_guest_image_tab, security_guest_image_load_guest_table, security_guest_image_item_click, security_guest_image_open_tab_manage_photo, security_guest_image_open_tab_add_photo, security_guest_image_setting_line_search, security_guest_image_item_image_click, security_guest_image_image_not_delete_click, security_guest_image_image_capture_click, security_guest_image_restore_image, security_guest_image_search
    from controllers.security_guest.security_guest_image_tab import security_guest_image_image_delete_click, security_guest_image_delete_image, security_guest_image_change_image_to_delete, security_guest_image_delete_image_capture, security_guest_image_add_image_capture, on_pushButton_guest_start_capture_clicked, security_guest_image_stop_camera_capture, on_pushButton_guest_capturing_clicked, security_guest_image_setting_button_capture, security_guest_image_clear_form_and_ui, security_guest_image_select_folder_image

    from controllers.security_access_control.security_access_control_controller import security_access_control_clear_form, load_security_access_control, security_access_control_handle_button, security_access_control_handle_combobox, security_access_control_combobox_setting, security_access_control_combobox_setting_data_change, security_access_control_handle_search_line_edit, security_access_control_table_widget_setting, security_access_control_button_setting_and_ui, security_access_control_open_tab_grant_role, security_access_control_open_tab_access_track
    
    from controllers.security_access_control.securety_access_control_grant_role_tab import security_access_control_grant_role_clear_form, security_access_control_grant_role_load, security_access_control_handle_button_grant_role_tab, security_access_control_handle_combobox_grant_role_tab, security_access_control_combobox_setting_grant_role_tab, security_access_control_combobox_setting_data_change_grant_role_tab, security_access_control_handle_search_line_edit_grant_role_tab, security_access_control_table_widget_setting_grant_role_tab
    from controllers.security_access_control.securety_access_control_grant_role_tab import security_access_control_button_setting_and_ui_grant_role_tab, security_access_control_grant_role_setting_line_search, security_access_control_grant_role_seach, security_access_control_grant_role_item_click, security_access_control_grant_role_export, security_access_control_grant_role_choose_file, security_access_control_grant_role_import_file, security_access_control_grant_role_add, security_access_control_grant_role_edit, security_access_control_grant_role_delete
    from controllers.security_access_control.securety_access_control_grant_role_tab import security_access_control_grant_role_setting_form, security_access_control_grant_role_combobox_data_change_building_search, security_access_control_grant_role_combobox_data_change_floor_search, security_access_control_grant_role_combobox_data_change_door_search, security_access_control_grant_role_combobox_data_change_building, security_access_control_grant_role_combobox_data_change_floor, security_access_control_grant_role_combobox_data_change_door, security_access_control_grant_role_combobox_data_change_permission

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Face Access Control")
        # for testing self.user_role = 1
        self.user_role = 2
        #self.user_role = 0
        self.database = db_connector.connector('localhost', 'henrydb', 'root', 'face_recognition')
        if self.database == None:
            msg = message_box.MyMessageBox(QMessageBox.Critical,"Wrong db or authentication", "You must change setting in .config file")
            sys.exit(msg.exec())
        self.thread = QThread()
        self.capture_image = video_stream.CaptureImage()
        self.images_capture = list()
        self.images_capture_guest = list()
        self.image_viewer = None
        self.flag_tab = None
        self.flag_anchor = None
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
        self.handle_tab_ui()

    def check_login(self):
        print(self.session)
        if self.session == None:
            sys.exit()
        if self.session == 'NoOne':
            self.handle_tab_ui()

    def handle_ui(self):
        # self.label_username_session.setStyleSheet("QLabel{font-family: ubuntu 30; color: blue; font-weight: bold}")
        self.tabWidget_main.tabBar().setVisible(False)
        self.tabWidget_building_manage.tabBar().setVisible(False)
        self.tabWidget_all.tabBar().setVisible(False)
        self.tabWidget_main_security.tabBar().setVisible(False)

    def handle_tab_ui(self):
        if self.user_role == 1:
            self.tabWidget_all.setCurrentIndex(0)
        elif self.user_role == 2:
            self.tabWidget_all.setCurrentIndex(2)
        else:
            self.tabWidget_all.setCurrentIndex(1)

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
        self.load_admin()
        self.load_security()

    def load_admin(self):
        self.load_building_manage()
        self.load_apartment_manage()
        self.load_resident_manage()
        self.load_guest_manage()
        self.load_access_control()
    
    def load_security(self):
        self.load_security_guest()
        self.load_security_access_control()
        
    def button_setting_and_ui(self):
        self.building_manage_button_setting_and_ui()
        self.apartment_manage_button_setting_and_ui()
        self.resident_manage_button_setting_and_ui()
        self.guest_manage_button_setting_and_ui()
        self.access_control_button_setting_and_ui()
        self.security_guest_button_setting_and_ui()

        
    def handle_buttons(self):
        self.handle_buttons_login_tab()
        self.handle_buttons_main_tab()
        self.handle_buttons_security_tab()
        #handle button for bulding manage
        self.building_manage_handle_button()
        self.apartment_manage_handle_button()
        self.resident_manage_handle_button()
        self.guest_manage_handle_button()
        self.access_control_handle_button()
        self.security_guest_handle_button()
        self.security_access_control_handle_button()

    def handle_buttons_main_tab(self):
        self.pushButton_buiding_manage.clicked.connect(self.open_tab_building)
        self.pushButton_apartment_manage.clicked.connect(self.open_tab_apartment)
        self.pushButton_resident_manage.clicked.connect(self.open_tab_resident)
        self.pushButton_gest_manage.clicked.connect(self.open_tab_guest)
        self.pushButton_video_access_control.clicked.connect(self.open_tab_access_control)
    
    def handle_buttons_security_tab(self):
        self.pushButton_video_access_control_security.clicked.connect(self.open_tab_security_access_control)
        self.pushButton_guest_management.clicked.connect(self.open_tab_security_guest_management)

    def handle_buttons_login_tab(self):
        self.pushButton_login.clicked.connect(self.login)
        self.lineEdit_password.returnPressed.connect(self.login)

    def handle_combobox(self):
        # handle action for combobox in buiding manage tab
        self.building_manage_handle_combobox()
        self.apartment_manage_handle_combobox()
        self.resident_manage_handle_combobox()
        self.guest_manage_handle_combobox()
        self.access_control_handle_combobox()
        self.security_guest_handle_combobox()
        self.security_access_control_handle_combobox()

    def combobox_setting(self):
        # setting combobox data for satatic combobox
        # setting for building manage tab
        self.building_manage_combobox_setting()
        self.apartment_manage_combobox_setting()
        self.resident_manage_combobox_setting()
        self.guest_manage_combobox_setting()
        self.access_control_combobox_setting()
        self.security_guest_combobox_setting()
        self.security_access_control_combobox_setting()

    def combobox_setting_data_change(self):
        self.building_manage_combobox_setting_data_change()
        self.apartment_manage_combobox_setting_data_change()
        self.resident_manage_combobox_setting_data_change()
        self.guest_manage_combobox_setting_data_change()
        self.access_control_combobox_setting_data_change()
        self.security_guest_combobox_setting_data_change()
        self.security_access_control_combobox_setting_data_change()

    # table widget setting
    def table_widget_setting(self):
        self.building_manage_table_widget_setting()
        self.apartment_manage_table_widget_setting()
        self.resident_manage_table_widget_setting()
        self.guest_manage_table_widget_setting()
        self.access_control_table_widget_setting()
        self.security_guest_table_widget_setting()
        self.security_access_control_table_widget_setting()

    def handle_search_line_edit(self):
        # handle line edit using for search
        # handle search line edit for building manage tab
        self.building_manage_handle_search_line_edit()
        self.apartment_manage_handle_search_line_edit()
        self.resident_manage_handle_search_line_edit()
        self.guest_manage_handle_search_line_edit()
        self.access_control_handle_search_line_edit()
        self.security_guest_handle_search_line_edit()
        self.security_access_control_handle_search_line_edit()

    def login(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        cursor = self.database.cursor()
        cursor.execute("select * from user where username='{}' and password='{}'".format(username, md5(password.encode()).hexdigest()))
        for i in range(cursor.rowcount):
            result = cursor.fetchall()
            if len(result) == 1:
                self.session = username
                self.user_role = result[0][3]
                cursor.close()
                break
        if self.session!= 'NoOne':
            self.login_clear_form()
            self.handle_tab_ui()
            self.load_data()
        else:
            self.label_error.setText('Wrong username or password')
    
    def logout(self):
        self.session = None
        self.user_role = 0
        self.handle_tab_ui()
        # To do: set all line, textedit to ''

    # open tab main

    # default init window
    def open_window(self):
        #for testing
        #self.check_login()
        #self.open_tab_building()
        self.open_tab_security_access_control()

    def open_tab_building(self):
        #for testing
        #self.check_login()
        self.flag_tab = '000'
        if self.flag_anchor and self.flag_anchor != self.flag_tab:
            warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.flag_anchor = None
                self.admin_clear_form()
                self.access_control_person_image_stop_camera_capture()

                self.tabWidget_main.setCurrentIndex(0)

                common.set_tab_when_clicked(self.pushButton_buiding_manage,
                self.pushButton_buiding_manage, self.pushButton_apartment_manage,
                self.pushButton_resident_manage, self.pushButton_gest_manage,
                self.pushButton_video_access_control)
                
                # setting current tab when the window first load
                self.tabWidget_building_manage.setCurrentIndex(0)
                common.set_tab_when_clicked(self.pushButton_block_manage, self.pushButton_floor_manage,
                self.pushButton_door_manage, self.pushButton_setting_manage)
        else:
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
        self.flag_tab = '010'
        if self.flag_anchor and self.flag_anchor != self.flag_tab:
            warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.flag_anchor = None
                self.admin_clear_form()
                self.access_control_person_image_stop_camera_capture()

                self.tabWidget_main.setCurrentIndex(1)

                common.set_tab_when_clicked(self.pushButton_apartment_manage,
                self.pushButton_buiding_manage, self.pushButton_apartment_manage,
                self.pushButton_resident_manage, self.pushButton_gest_manage,
                self.pushButton_video_access_control)

            
                self.tabWidget_apartment.setCurrentIndex(0)
                common.set_tab_when_clicked(self.pushButton_company_apartment_manage, self.pushButton_apartment_resident_manage)
        else:
            self.tabWidget_main.setCurrentIndex(1)

            common.set_tab_when_clicked(self.pushButton_apartment_manage,
            self.pushButton_buiding_manage, self.pushButton_apartment_manage,
            self.pushButton_resident_manage, self.pushButton_gest_manage,
            self.pushButton_video_access_control)

        
            self.tabWidget_apartment.setCurrentIndex(0)
            common.set_tab_when_clicked(self.pushButton_company_apartment_manage, self.pushButton_apartment_resident_manage)

    def open_tab_resident(self):
        self.flag_tab = '020'
        if self.flag_anchor and self.flag_anchor != self.flag_tab:
            warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.flag_anchor = None
                self.admin_clear_form()
                self.access_control_person_image_stop_camera_capture()

                self.tabWidget_main.setCurrentIndex(2)

                common.set_tab_when_clicked(self.pushButton_resident_manage,
                self.pushButton_buiding_manage, self.pushButton_apartment_manage,
                self.pushButton_resident_manage, self.pushButton_gest_manage,
                self.pushButton_video_access_control)
                common.set_tab_when_clicked(self.pushButton_company_staff, self.pushButton_resident)

                self.tabWidget_resident_manage.setCurrentIndex(0)
                common.set_tab_when_clicked(self.pushButton_company_staff, self.pushButton_resident)
        else:
            self.tabWidget_main.setCurrentIndex(2)

            common.set_tab_when_clicked(self.pushButton_resident_manage,
            self.pushButton_buiding_manage, self.pushButton_apartment_manage,
            self.pushButton_resident_manage, self.pushButton_gest_manage,
            self.pushButton_video_access_control)
            common.set_tab_when_clicked(self.pushButton_company_staff, self.pushButton_resident)

            self.tabWidget_resident_manage.setCurrentIndex(0)
            common.set_tab_when_clicked(self.pushButton_company_staff, self.pushButton_resident)

    def open_tab_guest(self):
        self.flag_tab = '030'
        if self.flag_anchor and self.flag_anchor != self.flag_tab:
            warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.flag_anchor = None
                self.admin_clear_form()
                self.access_control_person_image_stop_camera_capture()

                self.tabWidget_main.setCurrentIndex(3)

                common.set_tab_when_clicked(self.pushButton_gest_manage,
                self.pushButton_buiding_manage, self.pushButton_apartment_manage,
                self.pushButton_resident_manage, self.pushButton_gest_manage,
                self.pushButton_video_access_control)

        else:
            self.tabWidget_main.setCurrentIndex(3)

            common.set_tab_when_clicked(self.pushButton_gest_manage,
            self.pushButton_buiding_manage, self.pushButton_apartment_manage,
            self.pushButton_resident_manage, self.pushButton_gest_manage,
            self.pushButton_video_access_control)

    def open_tab_access_control(self):
        self.flag_tab = '040'
        if self.flag_anchor and self.flag_anchor != self.flag_tab:
            warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.flag_anchor = None
                self.admin_clear_form()
                self.access_control_person_image_stop_camera_capture()

                self.tabWidget_main.setCurrentIndex(4)

                common.set_tab_when_clicked(self.pushButton_video_access_control,
                self.pushButton_buiding_manage, self.pushButton_apartment_manage,
                self.pushButton_resident_manage, self.pushButton_gest_manage,
                self.pushButton_video_access_control)

                self.tabWidget_access_control.setCurrentIndex(0)
                common.set_tab_when_clicked(self.pushButton_grant_role, self.pushButton_person_image, self.pushButton_access_track)
        else:
            self.tabWidget_main.setCurrentIndex(4)

            common.set_tab_when_clicked(self.pushButton_video_access_control,
            self.pushButton_buiding_manage, self.pushButton_apartment_manage,
            self.pushButton_resident_manage, self.pushButton_gest_manage,
            self.pushButton_video_access_control)

            self.tabWidget_access_control.setCurrentIndex(0)
            common.set_tab_when_clicked(self.pushButton_grant_role, self.pushButton_person_image, self.pushButton_access_track)
    
    def clear_all_form(self):
        self.admin_clear_form()
        self.login_clear_form()
        self.security_clear_form()

    def admin_clear_form(self):
        self.admin_building_clear_form()
        self.admin_apartment_clear_form()
        self.admin_resident_clear_form()
        self.admin_guest_clear_form()
        self.admin_access_control_clear_form()

    def login_clear_form(self):
        self.lineEdit_username.setText('')
        self.lineEdit_password.setText('')
        self.label_error.setText('')

    def security_clear_form(self):
        self.security_guest_clear_form()
        self.security_access_control_clear_form()

    def open_tab_security_access_control(self):
        self.flag_tab = '210'
        if self.flag_anchor and self.flag_anchor != self.flag_tab:
            warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.flag_anchor = None
                self.security_clear_form()
                self.security_guest_image_stop_camera_capture()

                self.tabWidget_main_security.setCurrentIndex(0)

                common.set_tab_when_clicked(self.pushButton_video_access_control_security, self.pushButton_guest_management)

                self.tabWidget_access_control_security.setCurrentIndex(0)
                common.set_tab_when_clicked(self.pushButton_grant_role_security, self.pushButton_access_track_security)
        else:
            self.tabWidget_main_security.setCurrentIndex(0)

            common.set_tab_when_clicked(self.pushButton_video_access_control_security, self.pushButton_guest_management)

            self.tabWidget_access_control_security.setCurrentIndex(0)
            common.set_tab_when_clicked(self.pushButton_grant_role_security, self.pushButton_access_track_security)
        
    def open_tab_security_guest_management(self):
        self.flag_tab = '211'
        if self.flag_anchor and self.flag_anchor != self.flag_tab:
            warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if warning == QMessageBox.Yes:
                self.flag_anchor = None
                self.security_clear_form()
                self.security_guest_image_stop_camera_capture()

                self.tabWidget_main_security.setCurrentIndex(1)
                common.set_tab_when_clicked(self.pushButton_guest_management, self.pushButton_video_access_control_security)

                self.tabWidget_security_guest_management.setCurrentIndex(0)
                common.set_tab_when_clicked(self.pushButton_guest_visit, self.pushButton_guest_image)
        else:
            self.tabWidget_main_security.setCurrentIndex(1)
            common.set_tab_when_clicked(self.pushButton_guest_management, self.pushButton_video_access_control_security)

            self.tabWidget_security_guest_management.setCurrentIndex(0)
            common.set_tab_when_clicked(self.pushButton_guest_visit, self.pushButton_guest_image)