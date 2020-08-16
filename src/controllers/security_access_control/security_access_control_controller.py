from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from util import common, standardized, message_box

# access control tab function
def security_access_control_clear_form(self):
    self.security_access_control_grant_role_clear_form()
    # self.security_acesss_control_access_track_clear_form()

def load_security_access_control(self):
    self.security_access_control_grant_role_load()
    # self.security_access_control_access_track_load()

def security_access_control_handle_button(self):
    self.pushButton_grant_role_security.clicked.connect(self.security_access_control_open_tab_grant_role)
    self.pushButton_access_track_security.clicked.connect(self.security_access_control_open_tab_access_track)

    self.security_access_control_handle_button_grant_role_tab()
    # self.security_access_control_handle_button_access_track_tab()

def security_access_control_handle_combobox(self):
    self.security_access_control_handle_combobox_grant_role_tab()
    # self.security_access_control_handle_combobox_access_track_tab()

def security_access_control_combobox_setting(self):
    self.security_access_control_combobox_setting_grant_role_tab()
    # self.security_access_control_combobox_setting_access_track_tab()

def security_access_control_combobox_setting_data_change(self):
    self.security_access_control_combobox_setting_data_change_grant_role_tab()
    # self.security_access_control_combobox_setting_data_change_access_track_tab()

def security_access_control_handle_search_line_edit(self):
    self.security_access_control_handle_search_line_edit_grant_role_tab()
    # self.security_access_control_handle_search_line_edit_access_track_tab()

def security_access_control_table_widget_setting(self):
    self.tabWidget_access_control_security.tabBar().setVisible(False)
    self.security_access_control_table_widget_setting_grant_role_tab()
    # self.security_access_control_table_widget_setting_access_track_tab()

def security_access_control_button_setting_and_ui(self):
    self.security_access_control_button_setting_and_ui_grant_role_tab()
    # self.security_access_control_button_setting_and_ui_access_track_tab()

def security_access_control_open_tab_grant_role(self):
    self.flag_tab = '200'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.security_clear_form()
            self.security_access_control_person_image_stop_camera_capture()
            self.tabWidget_access_control_security.setCurrentIndex(0)
            common.set_tab_when_clicked(self.pushButton_grant_role_security, self.pushButton_access_track_security)
            self.load_security_access_control()   
    else:
        self.tabWidget_access_control_security.setCurrentIndex(0)
        common.set_tab_when_clicked(self.pushButton_grant_role_security, self.pushButton_access_track_security)
        self.load_security_access_control()

def security_access_control_open_tab_access_track(self):
    self.flag_tab = '201'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.security_clear_form()
            self.security_access_control_person_image_stop_camera_capture()
            self.tabWidget_access_control_security.setCurrentIndex(1)
            common.set_tab_when_clicked(self.pushButton_access_track_security, self.pushButton_grant_role_security)
            self.load_security_access_control()
    else:
        self.tabWidget_access_control_security.setCurrentIndex(1)
        common.set_tab_when_clicked(self.pushButton_access_track_security, self.pushButton_grant_role_security)
        self.load_security_access_control()