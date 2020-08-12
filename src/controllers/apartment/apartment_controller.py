from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

from util import common, standardized, message_box

# apartment manage tab funtion
def load_apartment_manage(self):
    self.apartment_manage_load_company_tab()
    self.apartment_manage_load_apartment_tab()

def apartment_manage_handle_button(self):
    self.pushButton_company_apartment_manage.clicked.connect(self.apartment_manage_open_tab_company)
    self.pushButton_apartment_resident_manage.clicked.connect(self.apartment_manage_open_tab_apartment)
    self.apartment_manage_handle_button_company_tab()
    self.apartment_manage_handle_button_apartment_tab()

def apartment_manage_handle_combobox(self):
    self.apartment_manage_handle_combobox_apartment_tab()
    self.apartment_manage_handle_combobox_company_tab()

def apartment_manage_combobox_setting(self):
    self.apartment_manage_combobox_setting_apartment_tab()
    self.apartment_manage_combobox_setting_company_tab()

#todo: load combobox have foreign key when it edit
def apartment_manage_combobox_setting_data_change(self):
    self.apartment_manage_combobox_setting_data_change_apartment_tab()
    self.apartment_manage_combobox_setting_data_change_company_tab()

def apartment_manage_handle_search_line_edit(self):
    self.apartment_manage_handle_search_line_edit_apartment_tab()
    self.apartment_manage_handle_search_line_edit_company_tab()

def apartment_manage_table_widget_setting(self):
    self.apartment_manage_table_widget_setting_apartment_tab()
    self.apartment_manage_table_widget_setting_company_tab()

def apartment_manage_button_setting_and_ui(self):
    self.tabWidget_apartment.tabBar().setVisible(False)
    self.apartment_manage_button_setting_and_ui_apartment_tab()
    self.apartment_manage_button_setting_and_ui_company_tab()

def apartment_manage_open_tab_company(self):
    self.tabWidget_apartment.setCurrentIndex(0)
    common.set_tab_when_clicked(self.pushButton_company_apartment_manage, self.pushButton_apartment_resident_manage)
    self.load_apartment_manage()

def apartment_manage_open_tab_apartment(self):
    self.tabWidget_apartment.setCurrentIndex(1)
    common.set_tab_when_clicked(self.pushButton_apartment_resident_manage, self.pushButton_company_apartment_manage)
    self.load_apartment_manage()