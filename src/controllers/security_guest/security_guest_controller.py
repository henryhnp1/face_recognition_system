from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from util import common, standardized, message_box

def security_guest_clear_form(self):
    self.security_guest_guest_visit_clear_form()

def load_security_guest(self):
    self.security_guest_guest_visit_load()

def security_guest_handle_button(self):
    self.pushButton_guest_visit.clicked.connect(self.security_guest_open_tab_guest_visit)
    self.pushButton_guest_image.clicked.connect(self.security_guest_open_tab_guest_image)
    # self.security_guest_handle_button_company_tab()
    self.security_guest_handle_button_guest_visit_tab()

def security_guest_handle_combobox(self):
    # self.security_guest_handle_combobox_apartment_tab()
    self.security_guest_handle_combobox_guest_visit_tab()

def security_guest_combobox_setting(self):
    # self.security_guest_combobox_setting_apartment_tab()
    self.security_guest_combobox_setting_guest_visit_tab()

#todo: load combobox have foreign key when it edit
def security_guest_combobox_setting_data_change(self):
    
    # self.security_guest_combobox_setting_data_change_apartment_tab()
    self.security_guest_combobox_setting_data_change_guest_visit_tab()

def security_guest_handle_search_line_edit(self):
    # self.security_guest_handle_search_line_edit_apartment_tab()
    self.security_guest_handle_search_line_edit_guest_visit_tab()

def security_guest_table_widget_setting(self):
    # self.security_guest_table_widget_setting_apartment_tab()
    self.security_guest_table_widget_setting_guest_visit_tab()

def security_guest_button_setting_and_ui(self):
    self.tabWidget_security_guest_management.tabBar().setVisible(False)
    # self.security_button_setting_and_ui_access_control_tab()
    self.security_guest_button_setting_and_ui_guest_visit_tab()

def security_guest_open_tab_guest_visit(self):
    self.flag_tab = '210'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.secutity_clear_form()
            # self.access_control_person_image_stop_camera_capture()
            self.tabWidget_security_guest_management.setCurrentIndex(0)
            common.set_tab_when_clicked(self.pushButton_guest_visit, self.pushButton_guest_image)
            self.load_security_guest()
    else:
        self.tabWidget_security_guest_management.setCurrentIndex(0)
        common.set_tab_when_clicked(self.pushButton_guest_visit, self.pushButton_guest_image)
        self.load_security_guest()

def security_guest_open_tab_guest_image(self):
    self.flag_tab = '211'
    if self.flag_anchor and self.flag_anchor != self.flag_tab:
        warning = QMessageBox.question(self, 'Warning', "Would you want to left this window and loss the data?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.flag_anchor = None
            self.secutity_clear_form()
            # self.access_control_person_image_stop_camera_capture()
            self.tabWidget_security_guest_management.setCurrentIndex(1)
            common.set_tab_when_clicked(self.pushButton_guest_image, self.pushButton_guest_visit)
            self.load_security_guest()
    else:
        self.tabWidget_security_guest_management.setCurrentIndex(1)
        common.set_tab_when_clicked(self.pushButton_guest_image, self.pushButton_guest_visit)
        self.load_security_guest()