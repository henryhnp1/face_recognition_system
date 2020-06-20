from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableView
import pandas as pd
import os

from util import common, standardized, message_box
from models import my_model

def building_manage_floor_manage_load(self, query=None):
    query = "select f.id, f.name, b.name as 'building', t.name as 'type of floor', f.number_of_apartment as 'number apartments' from floor as f, building as b, type_of_floor as t where f.building = b.id and f.type_of_floor = t.id order by b.name, f.id, t.name"
    common.data_loader(self, self.database, 'floor', self.tableWidget_floor, query)

def building_manage_handle_button_floor_manage_tab(self):
    self.building_manage_floor_manage_add_floor()
    self.building_manage_floor_manage_edit_floor()
    self.building_manage_floor_manage_delete_floor()
    self.building_manage_floor_manage_select_file_import_floor()
    self.building_manage_floor_manage_import_file_floor()

def building_manage_handle_combobox_floor_manage_tab(self):
    self.comboBox_search_floor.currentTextChanged.connect(self.building_manage_floor_manage_setting_line_search)

def building_manage_handle_search_line_edit_floor_tab(self):
    self.lineEdit_search_floor.returnPressed.connect(self.building_manage_floor_manage_search_floor)

def building_manage_combobox_setting_floor_manage_tab(self):
    fields_search = ['id', 'name', 'block', 'type_of_floor']
    self.comboBox_search_floor.addItems(fields_search)

    # todo after add any thing load all data

def building_manage_combobox_setting_data_change_floor_manage_tab(self):
    self.comboBox_floor_building.clear()

    self.comboBox_typeOfFloor.clear()

    cursor = self.database.cursor()
    query_select_building = "select * from building"
    query_select_type_of_floor = "select * from type_of_floor"

    cursor.execute(query_select_building)
    data_building = cursor.fetchall()
    field_building = []
    field_type_of_floor = []

    for building in data_building:
        field_building.append(building[1])
        building_object = my_model.Building(building[0], building[1], building[2], building[3], building[4])
        self.comboBox_floor_building.addItem(building[1], building_object)
    
    cursor.execute(query_select_type_of_floor)
    data_type_of_floor = cursor.fetchall()
    for type_of_floor in data_type_of_floor:
        field_type_of_floor.append(type_of_floor[1])

    # self.comboBox_floor_building.addItems(field_building)
    self.comboBox_typeOfFloor.addItems(field_type_of_floor)
    



def building_manage_floor_manage_tab_table_widget_setting(self):
    self.tableWidget_floor.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_floor.itemClicked.connect(self.building_manage_floor_manage_floor_item_click)
    self.tableWidget_floor.setSortingEnabled(True)

def building_manage_button_setting_and_ui_floor_tab(self):
    pass

def building_manage_floor_manage_setting_line_search(self):
    field_search = self.comboBox_search_floor.currentText()
    if field_search == 'id' or field_search == 'name':
        self.lineEdit_search_floor.setText('')
        self.lineEdit_search_floor.setValidator(QIntValidator(0, 100000, self))
    else:
        self.lineEdit_search_floor.setValidator(None)



def building_manage_floor_manage_search_floor(self):
    field_search = self.comboBox_search_floor.currentText()
    text_search = self.lineEdit_search_floor.text()
    query = "select f.id, f.name, b.name, t.name, f.number_of_apartment from floor as f inner join building as b on f.building = b.id inner join type_of_floor as t on f.type_of_floor = t.id {} order by b.name, f.id, t.name;"
    if field_search == 'id':
        query = query.format("where f.id = {}".format(int(text_search)))
    elif field_search == 'name':
        query = query.format("where f.name = {}".format(int(text_search)))
    elif field_search == 'block':
        query = query.format("where b.name like '%{}%'".format(text_search))
    else:
        query = query.format("where t.name like '%{}%'".format(text_search))
    common.data_loader(self, self.database, 'None', self.tableWidget_floor, query)

def building_manage_floor_manage_add_floor(self):
    pass

def building_manage_floor_manage_edit_floor(self):
    pass

def building_manage_floor_manage_delete_floor(self):
    pass

def building_manage_floor_manage_select_file_import_floor(self):
    pass

def building_manage_floor_manage_import_file_floor(self):
    pass

def building_manage_floor_manage_floor_item_click(self):
    current_row = self.tableWidget_floor.currentRow()
    columns_num = self.tableWidget_floor.columnCount()
    data = []
    for cell in range(0, columns_num):
        item = self.tableWidget_floor.item(current_row, cell).text()
        data.append(item)

    self.lineEdit_id_floor.setText(data[0])
    self.spinBox_name_floor.setValue(int(data[1]))
    # self.comboBox_floor_building.setValue(int(test[3]))
    # self.comboBox_typeOfFloor.setText(test[2] if test[2] !='None' else "")
    self.spinBox_numOfApartment.setValue(int(data[4]))

    t = self.comboBox_floor_building.currentData()
    print(t.pk)


def building_manage_floor_manage_combobox_building_selected(self, index):
    itemName = self.comboBox_floor_building.currentText()
    building_object = self.comboBox_floor_building.itemData(index)

def building_manage_floor_manage_clear_form(self):
    pass