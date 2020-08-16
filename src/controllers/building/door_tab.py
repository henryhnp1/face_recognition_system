from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox
import pandas as pd
import os
from PyQt5.QtCore import Qt
import MySQLdb as db

from util import common, standardized, message_box
from models import my_model

fully_query_door = '''
        select d.id, b.name as 'building', f.name as 'floor' , d.name as 'door', r.name as 'role' from door as d 
        join floor as f on d.floor = f.id 
        join building as b on f.building = b.id
        join role_door as r on d.role = r.id
    '''
def admin_building_door_clear_form(self):
    self.building_manage_door_manage_clear_role_door_form()
    self.building_manage_door_manage_clear_door_form()

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
    self.pushButton_add_door.clicked.connect(self.building_manage_door_manage_add_door)
    self.pushButton_edit_door.clicked.connect(self.building_manage_door_manage_edit_door)
    self.pushButton_delete_door.clicked.connect(self.building_manage_door_manage_delete_door)
    self.pushButton_select_file_door.clicked.connect(self.building_manage_door_manage_choose_file_door_import)
    self.pushButton_import_file_door.clicked.connect(self.building_manage_door_manage_import_file_door)
    self.pushButton_export_door.clicked.connect(self.building_manage_door_mange_export_file_door)
    self.pushButton_role_door_add.clicked.connect(self.building_manage_door_manage_add_role_door)
    self.pushButton_role_door_edit.clicked.connect(self.building_manage_door_manage_edit_role_door)
    self.pushButton_role_door_delete.clicked.connect(self.building_manage_door_manage_delete_role_door)

def building_manage_handle_combobox_door_manage_tab(self):

    self.comboBox_door_manage_building.currentTextChanged.connect(self.building_manage_combobox_setting_data_change_door_manage_tab_floor_combobox)
    self.comboBox_search_door.currentTextChanged.connect(self.building_manage_seach_line_edit_setting_search_door)
    self.comboBox_search_role_door.currentTextChanged.connect(self.building_manage_seach_line_edit_setting_search_role_door)

def building_manage_handle_search_line_edit_door_tab(self):
    self.lineEdit_search_door.returnPressed.connect(self.building_manage_door_manage_search_door)
    self.lineEdit_search_role_door.returnPressed.connect(self.building_manage_door_manage_search_role_door)

def building_manage_combobox_setting_door_manage_tab(self):
    self.comboBox_door_manage_floor.setEditable(True)
    self.comboBox_door_manage_floor.setFocusPolicy(Qt.StrongFocus)
    self.comboBox_door_manage_floor.completer().setCompletionMode(QCompleter.PopupCompletion)
    self.comboBox_door_manage_floor.setInsertPolicy(QComboBox.NoInsert)

    door_manage_combobox_fields = ['id', 'building', 'floor', 'door', 'role']
    self.comboBox_search_door.addItems(door_manage_combobox_fields)

    role_door_fields = ['id', 'name', 'description']
    self.comboBox_search_role_door.addItems(role_door_fields)
    
def building_manage_combobox_setting_data_change_door_manage_tab(self):
    self.building_manage_combobox_setting_data_change_door_manage_tab_building_combobox()
    
    self.building_manage_combobox_setting_data_change_door_manage_tab_role_door_combobox()

def building_manage_combobox_setting_data_change_door_manage_tab_building_combobox(self):
    self.comboBox_door_manage_building.clear()
    query_get_building = "select * from building"
    list_building = common.get_list_model(self.database, my_model.Building, query_get_building)
    for building in list_building:
        building_model = my_model.Building(*building)
        self.comboBox_door_manage_building.addItem(building[1], building_model)

def building_manage_combobox_setting_data_change_door_manage_tab_floor_combobox(self):
    building_object = self.comboBox_door_manage_building.currentData()
    if building_object:
        building_id = building_object.pk
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
    field_search = self.comboBox_search_door.currentText()
    text_search = self.lineEdit_search_door.text()
    query = '''
        select d.id, b.name as 'building', f.name as 'floor' , d.name as 'door', r.name as 'role' from door as d 
        join floor as f on d.floor = f.id 
        join building as b on f.building = b.id
        join role_door as r on d.role = r.id {}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("where d.id like '%{}%'".format(int(text_search)))
    elif field_search == 'floor':
        query = query.format("where f.name like '%{}%'".format(int(text_search)))
    elif field_search == 'door':
        query = query.format("where d.name like '%{}%'".format(int(text_search)))
    elif field_search == 'building':
        query = query.format("where b.name like '%{}%'".format(text_search))
    elif field_search == 'role':
        query = query.format("where r.name like '%{}%'".format(text_search))
    common.data_loader(self, self.database, 'None', self.tableWidget_door, query)

def building_manage_door_manage_search_role_door(self):
    field_search = self.comboBox_search_role_door.currentText()
    text_search = self.lineEdit_search_role_door.text()
    query = '''
        select * from role_door as r{}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("where r.id = {}".format(int(text_search)))
    elif field_search == 'name':
        query = query.format("where r.name like '%{}%'".format(text_search))
    elif field_search == 'description':
        query = query.format("where r.description like '%{}%'".format(text_search))
    common.data_loader(self, self.database, 'None', self.tableWidget_door, query)

def building_manage_door_manage_tab_table_widget_setting(self):
    self.tableWidget_door.setSortingEnabled(True)
    self.tableWidget_role_door.setSortingEnabled(True)
    self.tableWidget_door.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_role_door.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_door.itemClicked.connect(self.building_manage_door_manage_door_item_click)
    self.tableWidget_role_door.itemClicked.connect(self.building_manage_door_manage_role_door_item_click)

def building_manage_button_setting_and_ui_door_tab(self):
    self.pushButton_select_file_door.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
    self.pushButton_import_file_door.setEnabled(False)

def building_manage_door_manage_door_item_click(self):
    current_row = self.tableWidget_door.currentRow()
    columns_num = self.tableWidget_door.columnCount()
    data = []
    for cell in range(0, columns_num):
        item = self.tableWidget_door.item(current_row, cell).text()
        data.append(item)

    self.lineEdit_id_door.setText(data[0])
    self.spinBox_name_door.setValue(int(data[3]))

    building_index = self.comboBox_door_manage_building.findText(data[1])
    self.comboBox_door_manage_building.setCurrentIndex(building_index)
    
    role_door_index = self.comboBox_door_permission.findText(data[4])
    self.comboBox_door_permission.setCurrentIndex(role_door_index)
    
    building_name = data[1]
    floor_name = data[2]
    query_select_floor = "select f.id, f.name, b.name, f.type_of_floor, f.number_of_apartment from floor as f join building  as b on f.building = b.id where b.name = '{}'"
    list_floor = common.get_list_model(self.database, my_model.Floor, query_select_floor.format(building_name))
    for i, floor in enumerate(list_floor):
        if int(data[2]) == floor[1]:
            self.comboBox_door_manage_floor.setCurrentIndex(i)
            break


def building_manage_door_manage_role_door_item_click(self):
    current_row = self.tableWidget_role_door.currentRow()
    columns_num = self.tableWidget_role_door.columnCount()
    data = []
    for cell in range(0, columns_num):
        item = self.tableWidget_role_door.item(current_row, cell).text()
        data.append(item)

    self.lineEdit_role_door_id.setText(data[0])
    self.lineEdit_role_door_name.setText(data[1])
    self.textEdit_role_door_description.setPlainText(data[2])

def building_manage_seach_line_edit_setting_search_door(self):
    field_search = self.comboBox_search_door.currentText()
    if field_search == 'id' or field_search == 'door' or field_search=='floor':
        self.lineEdit_search_door.setText('')
        self.lineEdit_search_door.setValidator(QIntValidator(0, 100000, self))
    else:
        self.lineEdit_search_door.setValidator(None)

def building_manage_seach_line_edit_setting_search_role_door(self):
    field_search = self.comboBox_search_role_door.currentText()
    if field_search == 'id':
        self.lineEdit_search_role_door.setText('')
        self.lineEdit_search_role_door.setValidator(QIntValidator(0, 100000, self))
    else:
        self.lineEdit_search_role_door.setValidator(None)
    
def building_manage_door_manage_add_door(self):
    name_door = int(self.spinBox_name_door.value())
    if name_door >= 1:
        building = self.comboBox_door_manage_building.currentData().pk
        floor = self.comboBox_door_manage_floor.currentData().pk
        role_door = self.comboBox_door_permission.currentData().pk
        query = 'insert into door(name, floor, role) value (%s, %s, %s)'
        cursor = self.database.cursor()
        try:
            cursor.execute(query,(name_door, floor, role_door))
            self.database.commit()
            common.data_loader(self, self.database, 'door', self.tableWidget_door, fully_query_door)
        except db.Error as e:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The door Is Exist!").exec()
        cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of door must be bigger than 0").exec()

def building_manage_door_manage_edit_door(self):
    if self.lineEdit_id_door.text():
        door_id = int(self.lineEdit_id_door.text())
        name = int(self.spinBox_name_door.value())
        if name >= 1:
            floor = self.comboBox_door_manage_floor.currentData().pk
            role_door = self.comboBox_door_permission.currentData().pk
            query = 'update door set door.name = %s, door.floor = %s, door.role = %s where door.id = %s'
            cursor = self.database.cursor()
            try:
                cursor.execute(query,(name, floor, role_door, door_id))
                self.database.commit()
                common.data_loader(self, self.database, 'door', self.tableWidget_door, fully_query_door)
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The door Is Exist!").exec()
            cursor.close()
        else:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of door must be bigger than 0").exec()
    else:
        pass

def building_manage_door_manage_delete_door(self):
    if self.lineEdit_id_door.text():
        door_id = int(self.lineEdit_id_door.text())
        if door_id != 1:
            common.delete_item(self, 'door', self.database, door_id, self.building_manage_door_manage_load, self.building_manage_door_manage_clear_door_form)
        else:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "This Door Can't Remove").exec()
    else:
        pass

def building_manage_door_manage_choose_file_door_import(self):
    common.select_file_building_setting(self, self.pushButton_select_file_door, self.pushButton_import_file_door)

def building_manage_door_manage_import_file_door(self):
    file_path = self.pushButton_select_file_door.text()
    filename, file_extension = os.path.splitext(file_path)
    with open(file_path, mode='rb') as f:
        if file_extension == '.csv':
            reader = pd.read_csv(f)
        else:
            reader = pd.read_excel(f)
        header = reader.columns
        cursor = self.database.cursor()
        try:
            for index, row in reader.iterrows():
                floor = int(row['floor'])
                door = int(row['door'])
                role_door = row['permission']
                try:
                    query = "call insert_door_from_file(%s, %s, %s);"
                    cursor.execute(query, (floor, door, role_door))
                    print(cursor._last_executed )
                    self.database.commit()
                except db.Error as e:
                    print(e)
            cursor.close()
        except:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!").exec()
    self.building_manage_floor_manage_load()

def building_manage_door_manage_add_role_door(self):
    name_role_door = self.lineEdit_role_door_name.text()
    if name_role_door:
        desc = self.textEdit_role_door_description.toPlainText()
        query = "insert into role_door(name, description) value(%s, %s)"
        cursor = self.database.cursor()
        try:
            cursor.execute(query,(name_role_door.upper(), desc))
            self.database.commit()
            common.data_loader(self, self.database, 'role_door', self.tableWidget_role_door, "select * from role_door")
        except db.Error as e:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The role door Is Exist!").exec()
        cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of role door must be not null").exec()

def building_manage_door_manage_edit_role_door(self):
    role_door_id = self.lineEdit_role_door_id.text()
    if role_door_id:
        if int(role_door_id) in [1, 2]:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Role Door Can't Be Change").exec()
        else:
            role_door_id = int(role_door_id)
            name_role_door = self.lineEdit_role_door_name.text()
            if name_role_door:
                desc = self.textEdit_role_door_description.toPlainText()
                query = "update role_door set role_door.name = %s, role_door.description = %s where role_door.id = %s"
                cursor = self.database.cursor()
                try:
                    cursor.execute(query,(name_role_door.upper(), desc, role_door_id))
                    self.database.commit()
                    common.data_loader(self, self.database, 'role_door', self.tableWidget_role_door, "select * from role_door")
                except db.Error as e:
                    message_box.MyMessageBox(QMessageBox.Critical, "Error", "The role door Is Exist!").exec()
                cursor.close()
            else:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of role door must be not null").exec()

def building_manage_door_manage_delete_role_door(self):
    role_door_id = self.lineEdit_role_door_id.text()
    if role_door_id:
        role_door_id = int(role_door_id)
        if role_door_id in [1, 2]:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Role Door Can't Be Change").exec()
        else:
            common.delete_item(self, 'role_door', self.database, role_door_id, self.building_manage_door_manage_load, self.building_manage_door_manage_clear_role_door_form)

def building_manage_door_mange_export_file_door(self):
    path_file = common.select_file_export(self, self.pushButton_export_door)
    if path_file:
        common.export_data_from_table_widget(self, self.tableWidget_door, path_file)
        
def building_manage_door_manage_clear_door_form(self):
    self.lineEdit_id_door.setText(None)
    self.spinBox_name_door.setValue(0)
    self.comboBox_door_manage_building.setCurrentIndex(0)
    self.comboBox_door_permission.setCurrentIndex(0)
    self.comboBox_door_manage_floor.setCurrentIndex(0)
    self.pushButton_import_file_door.setEnabled(False)

def building_manage_door_manage_clear_role_door_form(self):
    self.lineEdit_role_door_id.setText(None)
    self.lineEdit_role_door_name.setText(None)
    self.textEdit_role_door_description.setPlainText(None)