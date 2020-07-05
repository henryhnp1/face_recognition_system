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
def apartment_manage_load_apartment_tab(self):
    common.data_loader(self, self.database, 'apartment', self.tableWidget_resident_apartment_table, fully_query_apartment)


def apartment_manage_handle_combobox_apartment_tab(self):
    self.comboBox_field_search_apartment.currentTextChanged.connect(self.apartment_manage_apartment_setting_line_search)
    self.comboBox_resident_apartment_block.currentTextChanged.connect(self.apartment_manage_setting_data_change_floor_combobox)
    self.comboBox_resident_apartment_floor.currentTextChanged.connect(self.apartment_manage_setting_data_change_prefix_apartment)
    self.apartment_manage_resident_mange_handle_spinbox()
def apartment_manage_handle_button_apartment_tab(self):
    self.pushButton_export_apartment.clicked.connect(self.apartment_manage_export_apartment)
    self.pushButton_select_file_apartment_resident_import.clicked.connect(self.apartment_manage_select_import_apartment)
    self.pushButton_import_resident_apartment.clicked.connect(self.apartment_manage_import_apartment)
    self.pushButton_resident_apartment_add.clicked.connect(self.apartment_manage_add_apartment)
    self.pushButton_resident_apartment_edit.clicked.connect(self.apartment_manage_edit_apartment)
    self.pushButton_resident_apartment_delete.clicked.connect(self.apartment_manage_delete_apartment)

def apartment_manage_combobox_setting_apartment_tab(self):
    field_apartment_search = ['id', 'building', 'floor', 'name', 'status']
    self.comboBox_field_search_apartment.addItems(field_apartment_search)

    field_apartment_status = ['Available', 'Not Available']
    self.comboBox_resident_apartment_status.addItems(field_apartment_status)

def apartment_manage_combobox_setting_data_change_apartment_tab(self):
    self.comboBox_resident_apartment_block.clear()
    query_get_building = "select * from building"
    list_building = common.get_list_model(self.database, my_model.Building, query_get_building)
    for building in list_building:
        building_model = my_model.Building(*building)
        self.comboBox_resident_apartment_block.addItem(building[1], building_model)


def apartment_manage_handle_search_line_edit_apartment_tab(self):
    self.lineEdit_line_search_apartment.returnPressed.connect(self.apartment_manage_search_apartment)

def apartment_manage_table_widget_setting_apartment_tab(self):
    self.tableWidget_resident_apartment_table.setSortingEnabled(True)
    self.tableWidget_resident_apartment_table.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_resident_apartment_table.itemClicked.connect(self.apartment_manage_apartment_item_click)

def apartment_manage_button_setting_and_ui_apartment_tab(self):
    self.pushButton_select_file_apartment_resident_import.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
    self.pushButton_import_resident_apartment.setEnabled(False)

def apartment_manage_setting_data_change_prefix_apartment(self):
    building_object = self.comboBox_resident_apartment_block.currentData()
    floor_object = self.comboBox_resident_apartment_floor.currentData()
    if building_object and floor_object:
        building_name = building_object.name
        floor_name = floor_object.name
        max_apartment = common.get_single_value_from_table('floor', 'number_of_apartment', 'where floor.name = {}'.format(floor_name), self.database)
        self.spinBox_apartment_number.setMaximum(int(max_apartment))
        if self.spinBox_apartment_number.value() < 10:
            temp_text = '00'
        else:
            temp_text = '0'
        self.label__prefix_apartment_number.setText(building_name+str(floor_name)+temp_text)

def apartment_manage_resident_manage_setting_prefix_apartment(self):
    current_prefix = self.label__prefix_apartment_number.text()
    if self.spinBox_apartment_number.value() > 9:
        if len(current_prefix) == 4:
            current_prefix = current_prefix[:3]
    else:
        if len(current_prefix) == 3:
            current_prefix = current_prefix + '0'
    self.label__prefix_apartment_number.setText(current_prefix)

def apartment_manage_setting_data_change_floor_combobox(self):
    building_object = self.comboBox_resident_apartment_block.currentData()
    if building_object:
        building_id = building_object.pk
        self.comboBox_resident_apartment_floor.clear()
        cursor = self.database.cursor()
        query_select_floor = '''
            select f.id, f.name as 'floor', b.name as 'building' ,t.name as 'type_of_floor', f.number_of_apartment as 'number_of_apartment' from floor as f
            join building as b on f.building = b.id
            join type_of_floor as t on f.type_of_floor = t.id
            where b.id = %s and t.name = 'resident'
        '''
        cursor.execute(query_select_floor, (building_id,))
        data_floor = cursor.fetchall()
        for floor in data_floor:
            floor_object = my_model.Floor(floor[0], floor[1], floor[2], floor[3], floor[4])
            floor_name = 'Tầng ' + str(floor[1]) + ' ' + floor[3]
            self.comboBox_resident_apartment_floor.addItem(floor_name, floor_object)

def apartment_manage_resident_mange_handle_spinbox(self):
    self.spinBox_apartment_number.textChanged.connect(self.apartment_manage_resident_manage_setting_prefix_apartment)

def apartment_manage_apartment_item_click(self):
    data = common.get_row_data_item_click(self.tableWidget_resident_apartment_table)

    self.lineEdit_id_resident_apartment.setText(data[0])
    building_index = self.comboBox_resident_apartment_block.findText(data[1])
    self.comboBox_resident_apartment_block.setCurrentIndex(building_index)

    office_status_index = self.comboBox_company_office_status.findText(data[4])
    self.comboBox_company_office_status.setCurrentIndex(office_status_index)

    office_name = data[3]
    self.spinBox_apartment_number.setValue(int(office_name[3:]))
    
    building_name = data[1]
    floor_name = data[2]
    query_select_floor = "select f.id, f.name, b.name, f.type_of_floor, f.number_of_apartment from floor as f join building  as b on f.building = b.id where b.name = '{}' and f.type_of_floor = 2"
    list_floor = common.get_list_model(self.database, my_model.Floor, query_select_floor.format(building_name))
    for i, floor in enumerate(list_floor):
        if int(data[2]) == floor[1]:
            self.comboBox_resident_apartment_floor.setCurrentIndex(i)
            break

def apartment_manage_apartment_setting_line_search(self):
    field_search = self.comboBox_field_search_apartment.currentText()
    if field_search == 'id' or field_search=='floor':
        self.lineEdit_line_search_apartment.setText('')
        self.lineEdit_line_search_apartment.setValidator(QIntValidator(0, 100000, self))
    else:
        self.lineEdit_line_search_apartment.setValidator(None)

def apartment_manage_search_apartment(self):
    field_search = self.comboBox_field_search_apartment.currentText()
    text_search = self.lineEdit_line_search_apartment.text()
    query = '''
        select a.id, b.name, f.name, a.name, if(a.status =0, 'Available', 'Not Available') as 'status' from apartment as a 
        join floor as f on f.id = a.floor
        join building as b on b.id = f.building
        join type_of_floor as t on f.type_of_floor = t.id
        where t.id = 2 {}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("and a.id like '%{}%'".format(int(text_search)))
    elif field_search == 'floor':
        query = query.format("and f.name like '%{}%'".format(int(text_search)))
    elif field_search == 'name':
        query = query.format("and a.name like '%{}%'".format((text_search)))
    elif field_search == 'building':
        query = query.format("and b.name like '%{}%'".format(text_search))
    elif field_search == 'status':
        if text_search in 'available':
            query = query.format("and a.status = 0".format(text_search))
        elif text_search in 'not availble':
            query = query.format("and a.status = 1".format(text_search))
        else:
            query = query.format('')
    common.data_loader(self, self.database, 'None', self.tableWidget_resident_apartment_table, query)

def apartment_manage_export_apartment(self):
    path_file = common.select_file_export(self, self.pushButton_export_apartment)
    if path_file:
        common.export_data_from_table_widget(self, self.tableWidget_resident_apartment_table, path_file)
        self.statusBar().showMessage("Export Success")

def apartment_manage_select_import_apartment(self):
    common.select_file_building_setting(self, self.pushButton_select_file_apartment_resident_import, self.pushButton_import_resident_apartment)

def apartment_manage_import_apartment(self):
    file_path = self.pushButton_select_file_apartment_resident_import.text()
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
                building = row['building']
                floor = int(row['floor'])
                apartment = row['apartment']
                status = row['status']
                try:
                    query = "call insert_apartment_from_file(%s, %s, %s, %s);"
                    cursor.execute(query, (building, floor, apartment ,status))
                    print(cursor._last_executed )
                    self.database.commit()
                except db.Error as e:
                    print(e)
            cursor.close()
        except:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!").exec()
    self.apartment_manage_load_company_tab()
    self.statusBar().showMessage("Import Success")

def apartment_manage_add_apartment(self):
    name_apartment = int(self.spinBox_apartment_number.value())
    if name_apartment >= 1:
        name_apartment = self.label__prefix_apartment_number.text() + str(name_apartment)
        building = self.comboBox_resident_apartment_block.currentData().pk
        floor = self.comboBox_resident_apartment_floor.currentData().pk
        status = self.comboBox_resident_apartment_status.currentText()
        if status == 'Available':
            status = 0
        else: status = 1
        query = 'insert into apartment(name, floor, status) value (%s, %s, %s)'
        cursor = self.database.cursor()
        try:
            cursor.execute(query,(name_apartment, floor, status))
            self.database.commit()
            common.data_loader(self, self.database, 'apartment', self.tableWidget_resident_apartment_table, fully_query_apartment)
        except db.Error as e:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The apartment Is Exist!").exec()
        cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of apartment must be bigger than 0").exec()

def apartment_manage_edit_apartment(self):
    if self.lineEdit_id_resident_apartment.text():
        apartment_id = int(self.lineEdit_id_resident_apartment.text())
        name = int(self.spinBox_apartment_number.value())
        if name >= 1:
            name = self.label__prefix_apartment_number.text() + str(name)
            floor = self.comboBox_resident_apartment_floor.currentData().pk
            status = self.comboBox_resident_apartment_status.currentText()
            if status == 'Available':
                status = 0
            else:
                status = 1
            query = 'update apartment set apartment.name = %s, apartment.floor = %s, apartment.status = %s where apartment.id = %s'
            cursor = self.database.cursor()
            try:
                cursor.execute(query,(name, floor, status, apartment_id))
                self.database.commit()
                common.data_loader(self, self.database, 'apartment', self.tableWidget_resident_apartment_table, fully_query_apartment)
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The apartment Is Exist!").exec()
            cursor.close()
        else:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of apartment must be bigger than 0").exec()
    else:
        pass

def apartment_manage_delete_apartment(self):
    if self.lineEdit_id_resident_apartment.text():
        apartment_id = int(self.lineEdit_id_resident_apartment.text())
        common.delete_item(self, 'apartment', self.database, apartment_id, self.apartment_manage_load_apartment_tab, self.apartment_manage_clear_apartment_form)

def apartment_manage_clear_apartment_form(self):
    self.lineEdit_id_resident_apartment.setText(None)
    self.comboBox_resident_apartment_block.setCurrentIndex(0)
    self.comboBox_resident_apartment_floor.setCurrentIndex(0)
    self.comboBox_resident_apartment_status.setCurrentIndex(0)
    self.pushButton_import_resident_apartment.setEnabled(False)