from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox
import pandas as pd
import os
from PyQt5.QtCore import Qt, QDate, QRegExp
import MySQLdb as db

from util import common, standardized, message_box
from models import my_model
full_select_staff = '''
    select s.id, c.name as 'company', a.name as 'office', p.name, p.birthday, if(p.gender=1,'Male', 'Female') as 'gender' ,
    p.id_card, p.phone, p.village, p.current_accommodation from company_staff as s
    join person as p on s.staff = p.id
    join company as c on s.company = c.id
    join apartment as a on a.id = c.apartment
    where p.is_delete = 0
'''
def resident_manage_staff_load(self):
    common.data_loader(self, self.database, 'None', self.tableWidget_staff_table, full_select_staff)

def resident_manage_handle_button_staff_tab(self):
    self.pushButton_export_staff.clicked.connect(self.resident_manage_staff_tab_export_file_staff)
    self.pushButton_select_company_staff_file.clicked.connect(self.resident_manage_staff_tab_sellect_file_import_staff)
    self.pushButton_import_company_staff.clicked.connect(self.resident_manage_staff_tab_import_file_staff)
    self.pushButton_company_staff_add.clicked.connect(self.resident_manage_staff_tab_add_staff)
    self.pushButton_company_staff_edit.clicked.connect(self.resident_manage_staff_tab_edit_staff)
    self.pushButton_company_staff_delete.clicked.connect(self.resident_manage_staff_tab_delete_staff)

def resident_manage_handle_combobox_staff_tab(self):
    self.comboBox_fields_search_company_staff.currentTextChanged.connect(self.resident_manage_staff_tab_setting_line_search)
    self.comboBox_company_staff_building.currentTextChanged.connect(self.resident_manage_staff_tab_data_change_floor_combobox)
    self.comboBox_company_staff_floor.currentTextChanged.connect(self.resident_manage_staff_tab_data_change_company_combobox)

def resident_manage_combobox_setting_staff_tab(self):
    field_search_staff = ['id', 'company', 'office', 'name', 'gender', 'id card', 'phone', 'village', 'current accommodation']
    self.comboBox_fields_search_company_staff.addItems(field_search_staff)

    field_gender = ['Male', 'Female']
    self.comboBox_company_staff_gender.addItems(field_gender)

def resident_manage_combobox_setting_data_change_staff_tab(self):
    self.resident_manage_staff_tab_data_change_building_combobox()

def resident_manage_handle_search_line_edit_staff_tab(self):
    self.lineEdit_search_company_staff.returnPressed.connect(self.resident_manage_staff_tab_search_staff)

def resident_manage_table_widget_setting_staff_tab(self):
    self.tableWidget_staff_table.setSortingEnabled(True)
    self.tableWidget_staff_table.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_staff_table.itemClicked.connect(self.resident_manage_staff_tab_item_click)

def resident_manage_button_setting_and_ui_staff_tab(self):
    self.pushButton_select_company_staff_file.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
    self.pushButton_import_company_staff.setEnabled(False)
    self.lineEdit_company_staff_id_number.setValidator(QRegExpValidator(QRegExp("[0-9]{9,12}")))
    self.lineEdit_company_staff_phone.setValidator(QRegExpValidator(QRegExp("[0-9]{10}")))

def resident_manage_staff_tab_setting_line_search(self):
    field_search = self.comboBox_fields_search_company_staff.currentText()
    if field_search == 'id' or field_search=='id card' or field_search == 'phone':
        self.lineEdit_search_company_staff.setText('')
        self.lineEdit_search_company_staff.setValidator(QIntValidator(0, 1000000000, self))
    else:
        self.lineEdit_search_company_staff.setValidator(None)

def resident_manage_staff_tab_search_staff(self):
    field_search = self.comboBox_fields_search_company_staff.currentText()
    text_search = self.lineEdit_search_company_staff.text()
    query = '''
        select s.id, c.name as 'company', a.name as 'office', p.name, p.birthday, if(p.gender=1,'Male', 'Female') as 'gender' ,
        p.id_card, p.phone, p.village, p.current_accommodation from company_staff as s
        join person as p on s.staff = p.id
        join company as c on s.company = c.id
        join apartment as a on a.id = c.apartment
        where p.is_delete = 0 {}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("and s.id like '%{}%'".format(int(text_search)))
    elif field_search == 'company':
        query = query.format("and c.name like '%{}%'".format(text_search))
    elif field_search == 'office':
        query = query.format("and a.name like '%{}%'".format(text_search))
    elif field_search == 'name':
        query = query.format("and p.name like '%{}%'".format(text_search))
    elif field_search == 'id card':
        query = query.format("and p.id_card like '%{}%'".format(text_search))
    elif field_search == 'gender':
        if text_search == 'male':
            query = query.format("and p.gender = 1")
        elif text_search == 'female':
            query = query.format("and p.gender = 0")
        else:
            query = query.format('')
    elif field_search == 'phone':
        query = query.format("and p.phone like '%{}%'".format(text_search))
    elif field_search == 'village':
        query = query.format("and p.village like '%{}%'".format(text_search))
    else:
        query = query.format("and p.current_accommodation like '%{}%'".format())
    common.data_loader(self, self.database, 'None', self.tableWidget_staff_table, query)

def resident_manage_staff_tab_add_staff(self):
    if self.lineEdit_company_staff_name.text() and self.lineEdit_company_staff_id_number.text():
        phone_number = self.lineEdit_company_staff_phone.text()
        id_number = self.lineEdit_company_staff_id_number.text()
        if (len(phone_number) > 0 and len(phone_number) <= 10) or (len(id_number) > 0 and (len(id_number) != 9) and len(id_number)!=12):
            if len(phone_number) > 0 and len(phone_number) <= 10:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Phone Must Be lenght 10").exec()
            else:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Must Be lenght = 9 or 13").exec()
        else:
            name = self.lineEdit_company_staff_name.text()
            birthday = self.dateEdit_company_staff_birthday.date()
            birthday_mysql = str(birthday.year()) + '-' +str(birthday.month()) + '-'+str(birthday.day())
            gender = self.comboBox_company_staff_gender.currentText()
            if gender == 'Male':
                gender = 1
            else: gender = 0
            id_number = self.lineEdit_company_staff_id_number.text()
            phone =self.lineEdit_company_staff_phone.text()
            village = self.textEdit_company_staff_village.toPlainText()
            curr_accommodation = self.textEdit_company_staff_current_accommodation.toPlainText()
            company = self.comboBox_company_staff_company.currentData().pk
            query = 'call insert_staff(%s, %s, %s, %s, %s, %s, %s, %s)'
            cursor = self.database.cursor()
            try:
                cursor.execute(query,(company, name, birthday, phone, id_number, village, curr_accommodation))
                self.database.commit()
                common.data_loader(self, self.database, 'None', self.tableWidget_staff_table, fully_query_apartment)
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Is Exist!").exec()
            cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name or ID Number must be Not Null").exec()

def resident_manage_staff_tab_edit_staff(self):
    if self.lineEdit_company_staff_name.text() and self.lineEdit_company_staff_id_number.text():
        phone_number = self.lineEdit_company_staff_phone.text()
        id_number = self.lineEdit_company_staff_id_number.text()
        if (len(phone_number) > 0 and len(phone_number) <= 10) or (len(id_number) > 0 and (len(id_number) != 9) and len(id_number)!=12):
            if len(phone_number) > 0 and len(phone_number) <= 10:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Phone Must Be lenght 10").exec()
            else:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Must Be lenght = 9 or 13").exec()
        else:
            name = self.lineEdit_company_staff_name.text()
            birthday = self.dateEdit_company_staff_birthday.date()
            birthday_mysql = str(birthday.year()) + '-' +str(birthday.month()) + '-'+str(birthday.day())
            gender = self.comboBox_company_staff_gender.currentText()
            if gender == 'Male':
                gender = 1
            else: gender = 0
            id_number = self.lineEdit_company_staff_id_number.text()
            phone =self.lineEdit_company_staff_phone.text()
            village = self.textEdit_company_staff_village.toPlainText()
            curr_accommodation = self.textEdit_company_staff_current_accommodation.toPlainText()
            company = self.comboBox_company_staff_company.currentData().pk
            query = 'call edit_staff(%s, %s, %s, %s, %s, %s, %s, %s)'
            cursor = self.database.cursor()
            try:
                cursor.execute(query,(company, name, birthday, phone, id_number, village, curr_accommodation))
                self.database.commit()
                common.data_loader(self, self.database, 'None', self.tableWidget_staff_table, fully_query_apartment)
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Is Exist!").exec()
            cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name or ID Number must be Not Null").exec()

def resident_manage_staff_tab_delete_staff(self):
    pass

def resident_manage_staff_tab_clear_form(self):
    self.lineEdit_company_staff_id.setText(None)
    self.lineEdit_company_staff_name.setText(None)
    self.dateEdit_company_staff_birthday.setDate(QDate().setDate(2000, 1, 1))
    self.comboBox_company_staff_gender.setCurrentIndex(0)
    self.lineEdit_company_staff_id_number.setText(None)
    self.lineEdit_company_staff_phone.setText(None)
    self.textEdit_company_staff_village.setPlainText(None)
    self.textEdit_company_staff_current_accommodation.setPlainText(None)
    self.comboBox_company_staff_building.setCurrentIndex(0)
    self.pushButton_select_company_staff_file.setText(None)
    self.pushButton_import_company_staff.setEnabled(False)

def resident_manage_staff_tab_sellect_file_import_staff(self):
    pass

def resident_manage_staff_tab_import_file_staff(self):
    pass

def resident_manage_staff_tab_export_file_staff(self):
    pass

def resident_manage_staff_tab_item_click(self):
    data = common.get_row_data_item_click(self.tableWidget_staff_table)
    self.lineEdit_company_staff_id.setText(data[0])
    self.lineEdit_company_staff_name.setText(data[3])
    gender_index = self.comboBox_company_staff_gender.findText(data[5])
    self.comboBox_company_staff_gender.setCurrentIndex(gender_index)
    self.lineEdit_company_staff_id_number.setText(data[6])
    if data[7] != 'None':
        self.lineEdit_company_staff_phone.setText(data[7])
    else:
        self.lineEdit_company_staff_phone.setText(None)
    self.textEdit_company_staff_village.setPlainText(data[8])
    self.textEdit_company_staff_current_accommodation.setPlainText(data[9])
    if data[4]:
        date_temp = data[4].split('-')
        birthday = QDate()
        birthday.setDate(int(date_temp[0]), int(date_temp[1]), int(date_temp[2]))
        self.dateEdit_company_staff_birthday.setDate(birthday)

    company_name = data[1]
    office_name = data[2]

    query_select_company_office_building = '''
        select c.id, c.name, a.id as 'office_id', a.name as 'office', f.id as 'floor_id', 
        f.name as 'floor', b.id as 'building_id', b.name as 'building' from company as c
        join apartment as a on c.apartment = a.id
        join floor as f on a.floor = f.id
        join building as b on b.id = f.building
        join type_of_floor as t on t.id = f.type_of_floor
        where t.name = 'business' and c.name = '{}' and a.name = '{}'
    '''
    list_company_office_building = common.get_list_model(self.database, my_model.Company_Office_Building, query_select_company_office_building.format(company_name, office_name))
    target = list_company_office_building[0]
    building_index = self.comboBox_company_staff_building.findText(target[7])
    self.comboBox_company_staff_building.setCurrentIndex(building_index)

    text_find = 'Tầng {} Tòa Nhà {}'.format(target[5], target[7])
    floor_index = self.comboBox_company_staff_floor.findText(text_find)
    self.comboBox_company_staff_floor.setCurrentIndex(floor_index)

    company_office_index = self.comboBox_company_staff_company.findText('Công Ty ' + str(target[1]) + ' Phòng ' + target[3])
    self.comboBox_company_staff_company.setCurrentIndex(company_office_index)

def resident_manage_staff_tab_data_change_building_combobox(self):
    self.comboBox_company_staff_building.clear()
    query_get_building = "select * from building"
    list_building = common.get_list_model(self.database, my_model.Building, query_get_building)
    for building in list_building:
        building_model = my_model.Building(*building)
        self.comboBox_company_staff_building.addItem(building[1], building_model)

def resident_manage_staff_tab_data_change_floor_combobox(self):
    building_object = self.comboBox_company_staff_building.currentData()
    if building_object:
        building_id = building_object.pk
        self.comboBox_company_staff_floor.clear()
        cursor = self.database.cursor()
        query_select_floor = '''
            select f.id, f.name as 'floor', b.name as 'building' ,t.name as 'type_of_floor', f.number_of_apartment as 'number_of_apartment' from floor as f
            join building as b on f.building = b.id
            join type_of_floor as t on f.type_of_floor = t.id
            where b.id = %s and t.id = 1
        '''
        cursor.execute(query_select_floor, (building_id,))
        data_floor = cursor.fetchall()
        for floor in data_floor:
            floor_object = my_model.Floor(floor[0], floor[1], floor[2], floor[3], floor[4])
            floor_name = 'Tầng ' + str(floor[1])+' Tòa Nhà ' + floor[2]
            self.comboBox_company_staff_floor.addItem(floor_name, floor_object)

def resident_manage_staff_tab_data_change_company_combobox(self):
    building_object = self.comboBox_company_staff_building.currentData()
    floor_object = self.comboBox_company_staff_floor.currentData()
    if building_object and floor_object:
        building_id = building_object.pk
        floor_id = floor_object.pk
        self.comboBox_company_staff_company.clear()
        cursor = self.database.cursor()
        query_select_floor = '''
            select c.id, c.name, c.phone, c.apartment, a.name as 'office'from company as c
            join apartment as a on c.apartment = a.id
            join floor as f on a.floor = f.id
            join building as b on b.id = f.building
            join type_of_floor as t on t.id = f.type_of_floor
            where t.id = 1 and b.id = %s and f.id = %s;
        '''
        cursor.execute(query_select_floor, (building_id, floor_id))
        data_company = cursor.fetchall()
        for company in data_company:
            company_object = my_model.Company(company[0], company[1], company[2], company[3], company[4])
            comapny_name = 'Công Ty ' + str(company[1]) + ' Phòng ' + company[4]
            self.comboBox_company_staff_company.addItem(comapny_name, company_object)
