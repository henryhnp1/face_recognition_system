from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox
import pandas as pd
import os
from PyQt5.QtCore import Qt
import MySQLdb as db

from util import common, standardized, message_box
from models import my_model

fully_query_office = '''
    select a.id, b.name as 'building', f.name as 'floor', a.name, if(a.status =0, 'Available', 'Not Available') as 'status' from apartment as a 
    join floor as f on a.floor = f.id
    join building as b on b.id = f.building
    join type_of_floor as t on t.id = f.type_of_floor
    where t.name = 'business'
'''
fully_query_company = '''
    select c.id, b.name as 'building', f.name as 'floor', a.name as 'apartment' ,c.name, c.phone from company as c
    join apartment as a on c.apartment = a.id
    join floor as f on a.floor = f.id
    join building as b on f.building = b.id
'''
def admin_apartment_company_clear_form(self):
    self.apartment_manage_clear_data_form_company_form()
    self.admin_apartment_company_office_clear_form()
    
def admin_apartment_company_office_clear_form(self):
    self.pushButton_select_file_company_office.setText("Choose file")
    self.pushButton_import_file_company_office.setEnabled(False)
    self.lineEdit_company_office_id.setText(None)
    self.comboBox_company_office_building.setCurrentIndex(0)
    self.comboBox_company_office_floor.setCurrentIndex(0)
    self.comboBox_company_office_status.setCurrentIndex(0)

def apartment_manage_load_company_tab(self):
    self.apartment_manage_load_company_tab_load_office_table()
    self.apartment_manage_load_company_tab_load_company_table()

def apartment_manage_handle_combobox_company_tab(self):
    self.comboBox_company_office_building.currentTextChanged.connect(self.apartment_manage_combobox_setting_data_change_company_tab_office_table_floor_combobox)
    self.comboBox_company_office_floor.currentTextChanged.connect(self.apartment_manage_set_prefix_office_number)

    self.comboBox_field_search_company_office.currentTextChanged.connect(self.apartment_manage_search_line_edit_setting_search_office)
    self.comboBox_field_search_company_apartment.currentTextChanged.connect(self.apartment_manage_search_line_edit_setting_search_company)

    self.comboBox_company_office_building_company.currentTextChanged.connect(self.apartment_manage_combobox_setting_data_change_company_tab_floor_combobox)
    self.comboBox_company_office_floor_company.currentTextChanged.connect(self.apartment_manage_combobox_setting_data_change_company_tab_office_combobox)
    
def apartment_manage_handle_button_company_tab(self):
    self.apartment_manage_handle_button_company_tab_office_table()
    self.apartment_manage_handle_button_company_tab_company_table()

def apartment_manage_handle_button_company_tab_office_table(self):
    self.pushButton_company_office_add.clicked.connect(self.apartment_manage_add_office)
    self.pushButton_company_office_edit.clicked.connect(self.apartment_manage_edit_office)
    self.pushButton_company_office_delete.clicked.connect(self.apartment_manage_delete_office)
    self.pushButton_select_file_company_office.clicked.connect(self.apartment_manage_select_file_import_office)
    self.pushButton_import_file_company_office.clicked.connect(self.apartment_manage_import_office)
    self.pushButton_export_office.clicked.connect(self.apartment_manage_export_office)

def apartment_manage_handle_button_company_tab_company_table(self):
    self.pushButton_company_add.clicked.connect(self.apartment_manage_add_company)
    self.pushButton_company_edit.clicked.connect(self.apartment_manage_edit_company)
    self.pushButton_company_delete.clicked.connect(self.apartment_manage_delete_company)
    self.pushButton_select_file_company.clicked.connect(self.apartment_manage_select_import_company)
    self.pushButton_import_file_company.clicked.connect(self.apartment_manage_import_company)
    self.pushButton_export_company.clicked.connect(self.apartment_manage_export_company)


def apartment_manage_combobox_setting_company_tab(self):
    field_search_office = ['id', 'building', 'floor', 'name', 'status']
    self.comboBox_field_search_company_office.addItems(field_search_office)

    field_of_status = ['Available', 'Not Available']
    self.comboBox_company_office_status.addItems(field_of_status)

    field_search_company = ['id', 'building','floor','office', 'name', 'phone']
    self.comboBox_field_search_company_apartment.addItems(field_search_company)

def apartment_manage_combobox_setting_data_change_company_tab(self):
    self.apartment_manage_combobox_setting_data_change_company_tab_office_table()
    self.apartment_manage_combobox_setting_data_change_company_tab_company_table()

def apartment_manage_handle_search_line_edit_company_tab(self):
    self.lineEdit_line_search_company_office.returnPressed.connect(self.apartment_manage_search_office)
    self.lineEdit_line_search_company_apartment.returnPressed.connect(self.apartment_manage_search_company)

def apartment_manage_table_widget_setting_company_tab(self):
    self.tableWidget_company_apartment_table.setSortingEnabled(True)
    self.tableWidget_company_apartment_table_office.setSortingEnabled(True)
    self.tableWidget_company_apartment_table.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_company_apartment_table_office.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_company_apartment_table.itemClicked.connect(self.apartment_manage_office_item_click)
    self.tableWidget_company_apartment_table_office.itemClicked.connect(self.apartment_manage_company_item_click)

def apartment_manage_button_setting_and_ui_company_tab(self):
    self.pushButton_select_file_company_office.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
    self.pushButton_import_file_company_office.setEnabled(False)
    self.pushButton_select_file_company.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
    self.pushButton_import_file_company.setEnabled(False)
    self.lineEdit_company_phone.setValidator(QIntValidator(0, 1147483647, self))

def apartment_manage_load_company_tab_load_office_table(self):
    common.data_loader(self, self.database, 'apartment', self.tableWidget_company_apartment_table, fully_query_office)

def apartment_manage_combobox_setting_data_change_company_tab_office_table(self):
    self.apartment_manage_combobox_setting_data_change_company_tab_office_table_block_combobox()
   

def apartment_manage_combobox_setting_data_change_company_tab_office_table_block_combobox(self):
    self.comboBox_company_office_building.clear()
    query_get_building = "select * from building"
    list_building = common.get_list_model(self.database, my_model.Building, query_get_building)
    for building in list_building:
        building_model = my_model.Building(*building)
        self.comboBox_company_office_building.addItem(building[1], building_model)

def apartment_manage_combobox_setting_data_change_company_tab_office_table_floor_combobox(self):
    building_object = self.comboBox_company_office_building.currentData()
    if building_object:
        building_id = building_object.pk
        self.comboBox_company_office_floor.clear()
        cursor = self.database.cursor()
        query_select_floor = '''
            select f.id, f.name as 'floor', b.name as 'building' ,t.name as 'type_of_floor', f.number_of_apartment as 'number_of_apartment' from floor as f
            join building as b on f.building = b.id
            join type_of_floor as t on f.type_of_floor = t.id
            where b.id = %s and t.name = 'business'
        '''
        cursor.execute(query_select_floor, (building_id,))
        data_floor = cursor.fetchall()
        for floor in data_floor:
            floor_object = my_model.Floor(floor[0], floor[1], floor[2], floor[3], floor[4])
            floor_name = 'Tầng ' + str(floor[1]) + ' ' + floor[3]
            self.comboBox_company_office_floor.addItem(floor_name, floor_object)

def apartment_manage_search_line_edit_setting_search_office(self):
    field_search = self.comboBox_field_search_company_office.currentText()
    if field_search == 'id' or field_search=='floor':
        self.lineEdit_line_search_company_office.setText('')
        self.lineEdit_line_search_company_office.setValidator(QIntValidator(0, 100000, self))
    else:
        self.lineEdit_line_search_company_office.setValidator(None)

def apartment_manage_search_line_edit_setting_search_company(self):
    field_search = self.comboBox_field_search_company_apartment.currentText()
    if field_search == 'id' or field_search=='phone':
        self.lineEdit_line_search_apartment.setText('')
        self.lineEdit_line_search_apartment.setValidator(QIntValidator(0, 1147483647, self))
    else:
        self.lineEdit_line_search_apartment.setValidator(None)

def apartment_manage_search_office(self):
    field_search = self.comboBox_field_search_company_office.currentText()
    text_search = self.lineEdit_line_search_company_office.text()
    query = '''
        select a.id, b.name as 'building', f.name as 'floor', a.name, if(a.status =0, 'Available', 'Not Available') as 'status' from apartment as a 
        join floor as f on a.floor = f.id
        join building as b on b.id = f.building
        join type_of_floor as t on t.id = f.type_of_floor
        where t.name = 'business' {}
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

def apartment_manage_office_item_click(self):
    data = common.get_row_data_item_click(self.tableWidget_company_apartment_table)

    self.lineEdit_company_office_id.setText(data[0])
    building_index = self.comboBox_company_office_building.findText(data[1])
    self.comboBox_company_office_building.setCurrentIndex(building_index)

    office_status_index = self.comboBox_company_office_status.findText(data[4])
    self.comboBox_company_office_status.setCurrentIndex(office_status_index)

    office_name = data[3]
    if office_name[3] == '0':
        self.label_spinbox_prefix.setText('0')
    else:
        self.label_spinbox_prefix.setText(None)

    self.spinBox__company_office_number.setValue(int(data[3][3:]))
    
    building_name = data[1]
    floor_name = data[2]
    query_select_floor = "select f.id, f.name, b.name, f.type_of_floor, f.number_of_apartment from floor as f join building  as b on f.building = b.id where b.name = '{}' and f.type_of_floor = 1"
    list_floor = common.get_list_model(self.database, my_model.Floor, query_select_floor.format(building_name))
    for i, floor in enumerate(list_floor):
        if int(data[2]) == floor[1]:
            self.comboBox_company_office_floor.setCurrentIndex(i)
            break

def apartment_manage_clear_data_form_office_form(self):
    self.lineEdit_company_office_id.setText(None)
    self.spinBox_name_door.setValue(0)
    self.comboBox_company_office_building.setCurrentIndex(0)
    self.comboBox_company_office_floor.setCurrentIndex(0)
    self.comboBox_company_office_status.setCurrentIndex(0)
    self.pushButton_import_file_company_office.setEnabled(False)
    self.label_prefix_office_number.setText(None)

def apartment_manage_set_prefix_office_number(self):
    building_object = self.comboBox_company_office_building.currentData()
    floor_object = self.comboBox_company_office_floor.currentData()
    if building_object and floor_object:
        building_name = building_object.name
        floor_name = floor_object.name
        max_apartment = common.get_single_value_from_table('floor', 'number_of_apartment', 'where floor.name = {}'.format(floor_name), self.database)
        self.spinBox__company_office_number.setMaximum(int(max_apartment))
        self.label_prefix_office_number.setText(building_name+str(floor_name)+'0')

def apartment_manage_add_office(self):
    name_office = int(self.spinBox__company_office_number.value())
    if name_office >= 1:
        if name_office >=10:
            name_office = self.label_prefix_office_number.text() + str(name_office)
        else:
            name_office = self.label_prefix_office_number.text()+ '0' + str(name_office)
        building = self.comboBox_door_manage_building.currentData().pk
        floor = self.comboBox_door_manage_floor.currentData().pk
        status = self.comboBox_company_office_status.currentText()
        if status == 'Available':
            status = 0
        else: status = 1
        query = 'insert into apartment(name, floor, status) value (%s, %s, %s)'
        cursor = self.database.cursor()
        try:
            cursor.execute(query,(name_office, floor, status))
            self.database.commit()
            common.data_loader(self, self.database, 'apartment', self.tableWidget_company_apartment_table, fully_query_office)
        except db.Error as e:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The apartment Is Exist!").exec()
        cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of door must be bigger than 0").exec()

def apartment_manage_edit_office(self):
    if self.lineEdit_company_office_id.text():
        office_id = int(self.lineEdit_company_office_id.text())
        name = int(self.spinBox__company_office_number.value())
        if name >= 1:
            if name >=10:
                name = self.label_prefix_office_number.text() + str(name)
            else:
                name = self.label_prefix_office_number.text()+ '0' + str(name)
            floor = self.comboBox_door_manage_floor.currentData().pk
            status = self.comboBox_company_office_status.currentText()
            if status == 'Available':
                status = 0
            else:
                status = 1
            query = 'update apartment set apartment.name = %s, apartment.floor = %s, apartment.status = %s where apartment.id = %s'
            cursor = self.database.cursor()
            try:
                cursor.execute(query,(name, floor, status, office_id))
                self.database.commit()
                common.data_loader(self, self.database, 'apartment', self.tableWidget_company_apartment_table, fully_query_office)
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The office Is Exist!").exec()
            cursor.close()
        else:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of office must be bigger than 0").exec()
    else:
        pass

def apartment_manage_delete_office(self):
    if self.lineEdit_company_office_id.text():
        office_id = int(self.lineEdit_company_office_id.text())
        common.delete_item(self, 'apartment', self.database, office_id, self.apartment_manage_load_company_tab, self.apartment_manage_clear_data_form_office_form)

def apartment_manage_select_file_import_office(self):
    common.select_file_building_setting(self, self.pushButton_select_file_company_office, self.pushButton_import_file_company_office)

def apartment_manage_import_office(self):
    file_path = self.pushButton_select_file_company_office.text()
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
                name = row['name']
                status = row['status']
                try:
                    query = "call insert_office_from_file(%s, %s, %s, %s);"
                    cursor.execute(query, (building, floor, name ,status))
                    print(cursor._last_executed )
                    self.database.commit()
                except db.Error as e:
                    print(e)
            cursor.close()
        except:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!").exec()
    self.apartment_manage_load_company_tab()

def apartment_manage_export_office(self):
    path_file = common.select_file_export(self, self.pushButton_export_office)
    if path_file:
        common.export_data_from_table_widget(self, self.tableWidget_company_apartment_table, path_file)
 #======================================================================================================       
def apartment_manage_load_company_tab_load_company_table(self):
    common.data_loader(self, self.database, 'company', self.tableWidget_company_apartment_table_office, fully_query_company)

def apartment_manage_combobox_setting_data_change_company_tab_company_table(self):
    self.comboBox_company_office_building_company.clear()
    query_get_building = "select * from building"
    list_building = common.get_list_model(self.database, my_model.Building, query_get_building)
    for building in list_building:
        building_model = my_model.Building(*building)
        self.comboBox_company_office_building_company.addItem(building[1], building_model)

def apartment_manage_combobox_setting_data_change_company_tab_floor_combobox(self):
    building_object = self.comboBox_company_office_building_company.currentData()
    if building_object:
        building_id = building_object.pk
        self.comboBox_company_office_floor_company.clear()
        cursor = self.database.cursor()
        query_select_floor = '''
            select f.id, f.name as 'floor', b.name as 'building' ,t.name as 'type_of_floor', f.number_of_apartment as 'number_of_apartment' from floor as f
            join building as b on f.building = b.id
            join type_of_floor as t on f.type_of_floor = t.id
            where b.id = %s and t.name = 'business'
        '''
        cursor.execute(query_select_floor, (building_id,))
        data_floor = cursor.fetchall()
        for floor in data_floor:
            floor_object = my_model.Floor(floor[0], floor[1], floor[2], floor[3], floor[4])
            floor_name = 'Tầng ' + str(floor[1]) + ' ' + floor[3]
            self.comboBox_company_office_floor_company.addItem(floor_name, floor_object)

def apartment_manage_combobox_setting_data_change_company_tab_office_combobox(self):
    floor_object = self.comboBox_company_office_floor_company.currentData()
    if floor_object:
        floor_id = floor_object.pk
        self.comboBox_company_office_number.clear()
        cursor = self.database.cursor()
        query_select_office = '''
            select * from apartment where apartment.floor = %s
        '''
        cursor.execute(query_select_office, (floor_id,))
        data_office = cursor.fetchall()
        for office in data_office:
            office_object = my_model.Apartment(office[0], office[1], office[2], office[3])
            if office[3] == 0:
                status = 'Available'
            else:
                status = 'Not Available'
            office_name = office[1] + ' ' + status
            self.comboBox_company_office_number.addItem(office_name, office_object)

def apartment_manage_company_item_click(self):
    data = common.get_row_data_item_click(self.tableWidget_company_apartment_table_office)

    self.lineEdit_company_id.setText(data[0])
    self.lineEdit_company_name.setText(data[4])
    self.lineEdit_company_phone.setText(data[5])

    building_index = self.comboBox_company_office_building_company.findText(data[1])
    self.comboBox_company_office_building_company.setCurrentIndex(building_index)
    
    building_name = data[1]
    floor_name = data[2]
    query_select_floor = "select a.id, a.name, a.floor, a.status from apartment as a join floor as f on a.floor = f.id where f.name = {}"
    list_office = common.get_list_model(self.database, my_model.Floor, query_select_floor.format(floor_name))
    for i, office in enumerate(list_office):
        if data[3] == office[1]:
            self.comboBox_company_office_number.setCurrentIndex(i)
            break
    
    floor_name = data[2]
    office_name = data[3]
    query_select_floor = "select f.id, f.name, b.name, f.type_of_floor, f.number_of_apartment from floor as f join building  as b on f.building = b.id where b.name = '{}' and f.type_of_floor = 1"
    list_floor = common.get_list_model(self.database, my_model.Floor, query_select_floor.format(building_name))
    for i, floor in enumerate(list_floor):
        if int(data[2]) == floor[1]:
            self.comboBox_company_office_floor_company.setCurrentIndex(i)
            break

def apartment_manage_search_company(self):
    field_search = self.comboBox_field_search_company_apartment.currentText()
    text_search = self.lineEdit_line_search_company_apartment.text()
    query = '''
        select c.id, b.name as 'building', f.name as 'floor', a.name as 'apartment' ,c.name, c.phone from company as c
        join apartment as a on c.apartment = a.id
        join floor as f on a.floor = f.id
        join building as b on f.building = b.id {}
    '''
    if text_search == '':
        query = query.format('')
        'id', 'building','floor','apartment', 'office number', 'phone'
    elif field_search == 'id':
        query = query.format("where c.id like '%{}%'".format(int(text_search)))
    elif field_search == 'floor':
        query = query.format("where f.name like '%{}%'".format(int(text_search)))
    elif field_search == 'name':
        query = query.format("where c.name like '%{}%'".format((ext_search)))
    elif field_search == 'building':
        query = query.format("where b.name like '%{}%'".format(text_search))
    elif field_search == 'office':
        query = query.format("where a.name like '%{}%'".format(text_search))
    else:
        query = query.format("where c.phone like '%{}%'".format(text_search))
    common.data_loader(self, self.database, 'None', self.tableWidget_company_apartment_table_office, query)

def apartment_manage_add_company(self):
    if self.lineEdit_company_name.text():
        name = self.lineEdit_company_name.text()
        phone = self.lineEdit_company_phone.text()
        floor = self.comboBox_company_office_floor_company.currentData().pk
        office = self.comboBox_company_office_number.currentText()
        if status == 'Available':
            status = 0
        else: status = 1
        query = 'call insert_company(%s, %s, %s)'
        cursor = self.database.cursor()
        try:
            cursor.execute(query,(name, phone, office))
            self.database.commit()
            common.data_loader(self, self.database, 'company', self.tableWidget_company_apartment_table, fully_query_office)
        except db.Error as e:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Company Is Exist!").exec()
        cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of company must be not null").exec()


def apartment_manage_edit_company(self):
    if self.lineEdit_company_id.text():
        company_id = int(self.lineEdit_company_id.text())
        if self.lineEdit_company_name.text():
            name = self.lineEdit_company_name.text()
            phone = self.lineEdit_company_phone.text()
            floor = self.comboBox_company_office_floor_company.currentData().pk
            office_new = self.comboBox_company_office_number.currentData().pk
            office_old = common.get_single_value_from_table('company', 'apartment', 'where id = {}'.format(company_id), self.database)
            query = 'call update_company(%s,%s, %s, %s, %s);'
            cursor = self.database.cursor()
            try:
                cursor.execute(query,(company_id, name, phone, office_old, office_new))
                self.database.commit()
                common.data_loader(self, self.database, 'company', self.tableWidget_company_apartment_table_office, fully_query_company)
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Company Is Exist!").exec()
            cursor.close()
        else:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of company must be not null").exec()

def apartment_manage_delete_company(self):
    if self.lineEdit_company_id.text():
        company_id = int(self.lineEdit_company_id.text())
        office_old = common.get_single_value_from_table('company', 'apartment', 'where id = {}'.format(company_id), self.database)
        query = 'update apartment set status = 0 where id = %s'
        cursor = self.database.cursor()
        try:
            cursor.execute(query,(office_old))
            self.database.commit()
            common.data_loader(self, self.database, 'apartment', self.tableWidget_company_apartment_table_office, fully_query_company)
        except db.Error as e:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "Wrong").exec()
        cursor.close()
        common.delete_item(self, 'company', self.database, company_id, self.apartment_manage_load_company_tab, self.apartment_manage_clear_data_form_company_form)


def apartment_manage_select_import_company(self):
    common.select_file_building_setting(self, self.pushButton_select_file_company, self.pushButton_import_file_company)

def apartment_manage_import_company(self):
    file_path = self.pushButton_select_file_company.text()
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
                office = row['office']
                name = row['name']
                phone = row['phone']
                try:
                    query = "call insert_company_from_file(%s, %s, %s, %s, %s);"
                    cursor.execute(query, (building, floor, office,name ,phone))
                    print(cursor._last_executed )
                    self.database.commit()
                except db.Error as e:
                    print(e)
            cursor.close()
        except:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!").exec()
    self.apartment_manage_load_company_tab()
    self.statusBar().showMessage("Import Success")

def apartment_manage_export_company(self):
    path_file = common.select_file_export(self, self.pushButton_export_company)
    if path_file:
        common.export_data_from_table_widget(self, self.tableWidget_company_apartment_table_office, path_file)
        self.statusBar().showMessage("Export Success")

def apartment_manage_clear_data_form_company_form(self):
    self.lineEdit_company_id.setText(None)
    self.lineEdit_company_name.setText(None)
    self.lineEdit_company_phone.setText(None)
    self.comboBox_company_office_building_company.setCurrentIndex(0)
    self.comboBox_company_office_floor_company.setCurrentIndex(0)
    self.comboBox_company_office_number.setCurrentIndex(0)
    self.pushButton_import_file_company.setEnabled(False)