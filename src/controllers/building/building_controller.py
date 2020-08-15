from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from util import common, standardized, message_box
def admin_building_clear_form(self):
    self.admin_building_block_clear_form()
    self.admin_building_door_clear_form()
    self.admin_building_floor_clear_form()
    self.admin_building_setting_clear_form()

def load_building_manage(self):
    self.building_manage_setting_load()
    self.building_manage_block_manage_load()
    self.building_manage_floor_manage_load()
    self.building_manage_door_manage_load()

    # open tab for building manage
def open_tab_block(self):
    self.flag_tab = '000'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.admin_clear_form()
            self.access_control_person_image_stop_camera_capture()
            self.tabWidget_building_manage.setCurrentIndex(0)

            common.set_tab_when_clicked(self.pushButton_block_manage,
                self.pushButton_setting_manage, self.pushButton_door_manage,
                self.pushButton_floor_manage, self.pushButton_block_manage)
            
            self.building_manage_block_manage_load()
    else:
        self.tabWidget_building_manage.setCurrentIndex(0)

        common.set_tab_when_clicked(self.pushButton_block_manage,
            self.pushButton_setting_manage, self.pushButton_door_manage,
            self.pushButton_floor_manage, self.pushButton_block_manage)
        
        self.building_manage_block_manage_load()

def open_tab_floor(self):
    self.flag_tab = '001'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.admin_clear_form()
            self.access_control_person_image_stop_camera_capture()
            self.tabWidget_building_manage.setCurrentIndex(1)

            common.set_tab_when_clicked(self.pushButton_floor_manage,
                self.pushButton_setting_manage, self.pushButton_door_manage,
                self.pushButton_floor_manage, self.pushButton_block_manage)

            self.building_manage_floor_manage_load()
    else:
        self.tabWidget_building_manage.setCurrentIndex(1)

        common.set_tab_when_clicked(self.pushButton_floor_manage,
            self.pushButton_setting_manage, self.pushButton_door_manage,
            self.pushButton_floor_manage, self.pushButton_block_manage)

        self.building_manage_floor_manage_load()

def open_tab_door(self):
    self.flag_tab = '002'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.admin_clear_form()
            self.access_control_person_image_stop_camera_capture()
            self.tabWidget_building_manage.setCurrentIndex(2)
            common.set_tab_when_clicked(self.pushButton_door_manage,
                self.pushButton_setting_manage, self.pushButton_door_manage,
                self.pushButton_floor_manage, self.pushButton_block_manage)
            
            self.building_manage_door_manage_load()
    else:
        self.tabWidget_building_manage.setCurrentIndex(2)
        common.set_tab_when_clicked(self.pushButton_door_manage,
            self.pushButton_setting_manage, self.pushButton_door_manage,
            self.pushButton_floor_manage, self.pushButton_block_manage)
        
        self.building_manage_door_manage_load()

def open_tab_setting(self):
    self.flag_tab = '003'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.admin_clear_form()
            self.access_control_person_image_stop_camera_capture()
            self.tabWidget_building_manage.setCurrentIndex(3)
            common.set_tab_when_clicked(self.pushButton_setting_manage,
                self.pushButton_setting_manage, self.pushButton_door_manage,
                self.pushButton_floor_manage, self.pushButton_block_manage)
            self.building_manage_setting_load()

    else:
        self.tabWidget_building_manage.setCurrentIndex(3)
        common.set_tab_when_clicked(self.pushButton_setting_manage,
            self.pushButton_setting_manage, self.pushButton_door_manage,
            self.pushButton_floor_manage, self.pushButton_block_manage)
        self.building_manage_setting_load()

def building_manage_button_setting_and_ui(self):
    self.building_manage_button_setting_and_ui_setting_tab()
    self.building_manage_button_setting_and_ui_block_tab()
    self.building_manage_button_setting_and_ui_floor_tab()
    self.building_manage_button_setting_and_ui_door_tab()

def building_manage_handle_combobox(self):
    self.building_manage_handle_combobox_setting_tab()
    self.building_manage_handle_combobox_block_manage_tab()
    self.building_manage_handle_combobox_floor_manage_tab()
    self.building_manage_handle_combobox_door_manage_tab()

def building_manage_table_widget_setting(self):
    self.building_manage_setting_tab_table_widget_setting()
    self.building_manage_block_manage_tab_table_widget_setting()
    self.building_manage_floor_manage_tab_table_widget_setting()
    self.building_manage_door_manage_tab_table_widget_setting()

def building_manage_combobox_setting(self):
    self.building_manage_combobox_setting_block_manage_tab()
    self.building_manage_combobox_setting_setting_tab()
    self.building_manage_combobox_setting_floor_manage_tab()
    self.building_manage_combobox_setting_door_manage_tab()

def building_manage_combobox_setting_data_change(self):
    self.building_manage_combobox_setting_data_change_block_manage_tab()
    self.building_manage_combobox_setting_data_change_setting_tab()
    self.building_manage_combobox_setting_data_change_floor_manage_tab()
    self.building_manage_combobox_setting_data_change_door_manage_tab()


def building_manage_handle_search_line_edit(self):
    self.building_manage_handle_search_line_edit_block_tab()
    self.building_manage_handle_search_line_edit_floor_tab()
    self.building_manage_handle_search_line_edit_door_tab()
    self.building_manage_handle_search_line_edit_setting_tab()

def building_manage_handle_button(self):
    #handle button for bulding manage
    self.pushButton_block_manage.clicked.connect(self.open_tab_block)
    self.pushButton_floor_manage.clicked.connect(self.open_tab_floor)
    self.pushButton_door_manage.clicked.connect(self.open_tab_door)
    self.pushButton_setting_manage.clicked.connect(self.open_tab_setting)

    self.building_manage_handle_button_setting_tab()
    self.building_manage_handle_button_block_manage_tab()
    self.building_manage_handle_button_floor_manage_tab()
    self.building_manage_handle_button_door_manage_tab()