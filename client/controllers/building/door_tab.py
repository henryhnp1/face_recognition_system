from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableView
import pandas as pd
import os

from util import common, standardized, message_box
from models import my_model

def building_manage_door_manage_load(self):
    pass
#     self.building_manage_door_manage_door_table_load()
#     self.building_manage_door_manage_role_door_table_load()
    
# def building_manage_door_manage_door_table_load(self, query=None):
#     common.data_loader(self, self.database, 'door', self.tableWidget_door, query)

# def building_manage_door_manage_role_door_table_load(self, query=None):
#     common.data_loader(self, self.table, 'role_door', self.tableWidget_role_door, query)

def building_manage_handle_button_door_manage_tab(self):
    pass

def building_manage_handle_combobox_door_manage_tab(self):
    pass

def building_manage_handle_search_line_edit_door_tab(self):
    self.lineEdit_search_door.returnPressed.connect(self.building_manage_door_manage_search_door)

def building_manage_combobox_setting_door_manage_tab(self):
    pass

def building_manage_combobox_setting_data_change_door_manage_tab(self):
    pass

def building_manage_door_manage_search_door(self):
    pass

def building_manage_door_manage_tab_table_widget_setting(self):
    pass

def building_manage_button_setting_and_ui_door_tab(self):
    pass
