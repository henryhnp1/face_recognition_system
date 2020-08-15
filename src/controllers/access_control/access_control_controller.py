from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from util import common, standardized, message_box

# access control tab function
def admin_access_control_clear_form(self):
    self.admin_access_control_grant_role_clear_form()
    self.admin_access_control_person_image_clear_form()
    self.admin_acesss_control_access_track_clear_form()

def load_access_control(self):
    self.access_control_grant_role_load()
    self.access_control_person_image_load()
    self.access_control_access_track_load()

def access_control_handle_button(self):
    self.pushButton_grant_role.clicked.connect(self.access_control_open_tab_grant_role)
    self.pushButton_person_image.clicked.connect(self.access_control_open_tab_person_image)
    self.pushButton_access_track.clicked.connect(self.access_control_open_tab_access_track)

    self.access_control_handle_button_grant_role_tab()
    self.access_control_handle_button_person_image_tab()
    self.access_control_handle_button_access_track_tab()

def access_control_handle_combobox(self):
    self.access_control_handle_combobox_grant_role_tab()
    self.access_control_handle_combobox_person_image_tab()
    self.access_control_handle_combobox_access_track_tab()

def access_control_combobox_setting(self):
    self.access_control_combobox_setting_grant_role_tab()
    self.access_control_combobox_setting_person_image_tab()
    self.access_control_combobox_setting_access_track_tab()

def access_control_combobox_setting_data_change(self):
    self.access_control_combobox_setting_data_change_grant_role_tab()
    self.access_control_combobox_setting_data_change_person_image_tab()
    self.access_control_combobox_setting_data_change_access_track_tab()

def access_control_handle_search_line_edit(self):
    self.access_control_handle_search_line_edit_grant_role_tab()
    self.access_control_handle_search_line_edit_person_image_tab()
    self.access_control_handle_search_line_edit_access_track_tab()

def access_control_table_widget_setting(self):
    self.tabWidget_access_control.tabBar().setVisible(False)
    self.access_control_table_widget_setting_grant_role_tab()
    self.access_control_table_widget_setting_person_image_tab()
    self.access_control_table_widget_setting_access_track_tab()

def access_control_button_setting_and_ui(self):
    self.access_control_button_setting_and_ui_grant_role_tab()
    self.access_control_button_setting_and_ui_person_image_tab()
    self.access_control_button_setting_and_ui_access_track_tab()

def access_control_open_tab_grant_role(self):
    self.flag_tab = '040'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.admin_clear_form()
            self.access_control_person_image_stop_camera_capture()
            self.tabWidget_access_control.setCurrentIndex(0)
            common.set_tab_when_clicked(self.pushButton_grant_role, self.pushButton_person_image, self.pushButton_access_track)
            self.load_access_control()   
    else:
        self.tabWidget_access_control.setCurrentIndex(0)
        common.set_tab_when_clicked(self.pushButton_grant_role, self.pushButton_person_image, self.pushButton_access_track)
        self.load_access_control()

def access_control_open_tab_person_image(self):
    self.flag_tab = '041'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.admin_clear_form()
            self.tabWidget_access_control.setCurrentIndex(1)
            common.set_tab_when_clicked(self.pushButton_person_image, self.pushButton_grant_role, self.pushButton_access_track)
            self.load_access_control()

            self.tabWidget_person_image_manage.setCurrentIndex(0)
            common.set_tab_when_clicked(self.pushButton_person_manage_manage_photo, self.pushButton_person_manage_add_photo)
            self.access_control_person_image_load()
    else:
        self.tabWidget_access_control.setCurrentIndex(1)
        common.set_tab_when_clicked(self.pushButton_person_image, self.pushButton_grant_role, self.pushButton_access_track)
        self.load_access_control()

        self.tabWidget_person_image_manage.setCurrentIndex(0)
        common.set_tab_when_clicked(self.pushButton_person_manage_manage_photo, self.pushButton_person_manage_add_photo)
        self.access_control_person_image_load()

def access_control_open_tab_access_track(self):
    self.flag_tab = '042'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.admin_clear_form()
            self.access_control_person_image_stop_camera_capture()
            self.tabWidget_access_control.setCurrentIndex(2)
            common.set_tab_when_clicked(self.pushButton_access_track, self.pushButton_person_image, self.pushButton_grant_role)
            self.load_access_control()
    else:
        self.tabWidget_access_control.setCurrentIndex(2)
        common.set_tab_when_clicked(self.pushButton_access_track, self.pushButton_person_image, self.pushButton_grant_role)
        self.load_access_control()