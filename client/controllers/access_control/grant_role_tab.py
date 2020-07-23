from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox
import pandas as pd
import os
from PyQt5.QtCore import Qt
import MySQLdb as db

from util import common, standardized, message_box
from models import my_model

fully_query_apartment = '''
    select a.id, b.name, f.name, a.name, if(a.status =0, 'Available', 'Not Available') as 'status' from apartment as a 
    join floor as f on f.id = a.floor
    join building as b on b.id = f.building
    join type_of_floor as t on f.type_of_floor = t.id
    where t.id = 2
'''

def access_control_grant_role_load(self):
    pass

def access_control_handle_button_grant_role_tab(self):
    pass

def access_control_handle_combobox_grant_role_tab(self):
    pass

def access_control_combobox_setting_grant_role_tab(self):
    pass

def access_control_combobox_setting_data_change_grant_role_tab(self):
    pass

def access_control_handle_search_line_edit_grant_role_tab(self):
    pass

def access_control_table_widget_setting_grant_role_tab(self):
    pass

def access_control_button_setting_and_ui_grant_role_tab(self):
    pass