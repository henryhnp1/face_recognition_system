from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox
import pandas as pd
import os
from PyQt5.QtCore import Qt

from util import common, standardized, message_box
from models import my_model

def building_manage_door_manage_load(self):
    self.building_manage_door_manage_door_table_load()
    self.building_manage_door_manage_role_door_table_load()
    
def building_manage_door_manage_door_table_load(self, query=None):
    query = '''
        select d.id, b.name as 'building', f.name as 'floor' , d.name as 'door', r.name as 'role' from door as d 
        join floor as f on d.floor = f.id 
        join building as b on f.building = b.id
        join role_door as r on d.role = r.id
    '''
    common.data_loader(self, self.database, 'door', self.tableWidget_door, query)

def building_manage_door_manage_role_door_table_load(self, query=None):
    common.data_loader(self, self.database, 'role_door', self.tableWidget_role_door, query)

def building_manage_handle_button_door_manage_tab(self):
    pass

def building_manage_handle_combobox_door_manage_tab(self):
    self.comboBox_door_manage_building.currentTextChanged.connect(self.building_manage_combobox_setting_data_change_door_manage_tab_floor_combobox)
    pass

def building_manage_handle_search_line_edit_door_tab(self):
    self.lineEdit_search_door.returnPressed.connect(self.building_manage_door_manage_search_door)

def building_manage_combobox_setting_door_manage_tab(self):
    self.comboBox_door_manage_floor.setEditable(True)
    self.comboBox_door_manage_floor.setFocusPolicy(Qt.StrongFocus)
    self.comboBox_door_manage_floor.completer().setCompletionMode(QCompleter.PopupCompletion)
    self.comboBox_door_manage_floor.setInsertPolicy(QComboBox.NoInsert)
    
def building_manage_combobox_setting_data_change_door_manage_tab(self):
    self.building_manage_combobox_setting_data_change_door_manage_tab_building_combobox()
    
    self.building_manage_combobox_setting_data_change_door_manage_tab_role_door_combobox()

def building_manage_combobox_setting_data_change_door_manage_tab_building_combobox(self):
    self.comboBox_door_manage_building.clear()
    query_get_building = "select * from building"
    list_building = common.get_list_model(self.database, my_model.Building, query_get_building)
    for building in list_building:
        self.comboBox_door_manage_building.addItem(building[1], building)

def building_manage_combobox_setting_data_change_door_manage_tab_floor_combobox(self):
    building_object = self.comboBox_door_manage_building.currentData()
    if building_object:
        building_id = building_object[0]
        self.comboBox_door_manage_floor.clear()
        cursor = self.database.cursor()
        query_select_floor = '''
            select f.id, f.name as 'floor', b.name as 'building' ,t.name as 'type_of_floor', f.number_of_apartment as 'number_of_apartment' from floor as f
            join building as b on f.building = b.id
            join type_of_floor as t on f.type_of_floor = t.id
            where b.id = %s
        '''
        cursor.execute(query_select_floor, (building_id,))
        data_floor = cursor.fetchall()
        for floor in data_floor:
            floor_object = my_model.Floor(floor[0], floor[1], floor[2], floor[3], floor[4])
            floor_name = 'Tầng ' + str(floor[1]) + ' ' + floor[3]
            self.comboBox_door_manage_floor.addItem(floor_name, floor_object)

def building_manage_combobox_setting_data_change_door_manage_tab_role_door_combobox(self):
    self.comboBox_door_permission.clear()
    cursor = self.database.cursor()
    query_select_role_door = "select * from role_door"
    cursor.execute(query_select_role_door)
    data_role_door = cursor.fetchall()
    for role_door in data_role_door:
        role_door_object = my_model.RoleDoor(role_door[0], role_door[1], role_door[2])
        self.comboBox_door_permission.addItem(role_door[1], role_door_object)

def building_manage_door_manage_search_door(self):
    pass

def building_manage_door_manage_tab_table_widget_setting(self):
    self.tableWidget_door.setSortingEnabled(True)
    self.tableWidget_role_door.setSortingEnabled(True)
    self.tableWidget_door.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_role_door.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_door.itemClicked.connect(self.building_manage_door_manage_door_item_click)
    self.tableWidget_role_door.itemClicked.connect(self.building_manage_door_manage_role_door_item_click)

def building_manage_button_setting_and_ui_door_tab(self):
    pass

def building_manage_door_manage_door_item_click(self):
    current_row = self.tableWidget_door.currentRow()
    columns_num = self.tableWidget_door.columnCount()
    data = []
    for cell in range(0, columns_num):
        item = self.tableWidget_door.item(current_row, cell).text()
        data.append(item)

    self.lineEdit_id_door.setText(data[0])

    query = "select * from building"
    list_model = common.get_list_model(self.database, my_model.Building, query)

    for i, model in enumerate(list_model):
        if data[0] == model[0]:
            self.comboBox_floor_building.setCurrentIndex(i)
            break
    
    # todo change how to don't need query
    query1 = "select * from role_door"
    list_role_door = common.get_list_model(self.database, my_model.RoleDoor, query1)
    for i, model in enumerate(list_tfl):
        if data[3] == model[1]:
            self.comboBox_door_permission.setCurrentIndex(i)
            break

def building_manage_door_manage_role_door_item_click(self):
    pass