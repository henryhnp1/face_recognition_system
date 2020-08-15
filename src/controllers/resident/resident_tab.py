from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox
import pandas as pd
import os
from PyQt5.QtCore import Qt, QRegExp, QDate
import MySQLdb as db

from util import common, standardized, message_box
from models import my_model

fully_query_resident = '''
    select p.id, a.name as 'apartment', p.name, p.birthday, 
    if(p.gender=1, 'Male', 'Female') as 'gender', p.id_card, 
    p.phone, p.village, p.current_accommodation  from person as p
    join resident_apartment as r on p.id = r.resident
    join apartment as a on a.id = r.apartment
    join floor as f on a.floor = f.id
    join building as b on b.id = f.building
    join type_of_floor as t on t.id = 2
    where p.is_delete = 0 and p.is_resident = 1
'''

def resident_manage_resident_load(self):
    common.data_loader(self, self.database, 'None', self.tableWidget_resident, fully_query_resident)

def resident_manage_handle_button_resident_tab(self):
    self.pushButton_export_resident.clicked.connect(self.resident_manage_resident_tab_export_file_resident)
    self.pushButton_select_resident.clicked.connect(self.resident_manage_resident_tab_select_file_import_resident)
    self.pushButton_import_resident.clicked.connect(self.resident_manage_resident_tab_import_file_resident)
    self.pushButton_resident_add.clicked.connect(self.resident_manage_resident_tab_add_resident)
    self.pushButton_resident_edit.clicked.connect(self.resident_manage_resident_tab_edit_resident)
    self.pushButton_resident_delete.clicked.connect(self.resident_manage_resident_tab_delete_resident)

def resident_manage_handle_combobox_resident_tab(self):
    self.comboBox_fields_search_resident.currentTextChanged.connect(self.resident_manage_resident_tab_setting_line_search)
    self.comboBox_resident_building.currentTextChanged.connect(self.resident_manage_resident_tab_data_change_floor_combobox)
    self.comboBox_resident_floor.currentTextChanged.connect(self.resident_manage_resident_tab_data_change_apartment_combobox)


def resident_manage_combobox_setting_resident_tab(self):
    field_search_resident = ['id', 'room', 'name', 'gender', 'id card', 'phone', 'village', 'current accommodation']
    self.comboBox_fields_search_resident.addItems(field_search_resident)

    field_gender = ['Male', 'Female']
    self.comboBox_resident_gender.addItems(field_gender)

def resident_manage_combobox_setting_data_change_resident_tab(self):
    self.resident_manage_resident_tab_data_change_building_combobox()

def resident_manage_handle_search_line_edit_resident_tab(self):
    self.lineEdit_search_resident.returnPressed.connect(self.resident_manage_resident_tab_search_resident)

def resident_manage_table_widget_setting_resident_tab(self):
    self.tableWidget_resident.setSortingEnabled(True)
    self.tableWidget_resident.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_resident.itemClicked.connect(self.resident_manage_resident_tab_item_click)

def resident_manage_button_setting_and_ui_resident_tab(self):
    self.pushButton_select_resident.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
    self.pushButton_import_resident.setEnabled(False)
    self.lineEdit_resident_id_number.setValidator(QRegExpValidator(QRegExp("[0-9]{9,12}")))
    self.lineEdit_resident_phone.setValidator(QRegExpValidator(QRegExp("[0-9]{10}")))

def resident_manage_resident_tab_setting_line_search(self):
    field_search = self.comboBox_fields_search_resident.currentText()
    if field_search == 'id' or field_search=='id card' or field_search == 'phone':
        self.lineEdit_search_resident.setText('')
        self.lineEdit_search_resident.setValidator(QRegExpValidator(QRegExp("[0-9]{9,12}")))
    else:
        self.lineEdit_search_resident.setValidator(None)

def resident_manage_resident_tab_search_resident(self):
    field_search = self.comboBox_fields_search_resident.currentText()
    text_search = self.lineEdit_search_resident.text()
    query = '''
        select p.id, a.name as 'apartment', p.name, p.birthday, 
        if(p.gender=1, 'Male', 'Female') as 'gender', p.id_card, 
        p.phone, p.village, p.current_accommodation  from person as p
        join resident_apartment as r on p.id = r.resident
        join apartment as a on a.id = r.apartment
        join floor as f on a.floor = f.id
        join building as b on b.id = f.building
        join type_of_floor as t on t.id = 2
        where p.is_delete = 0 and p.is_resident = 1 {}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("and s.id like '%{}%'".format(int(text_search)))
    elif field_search == 'room':
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
        query = query.format("and p.current_accommodation like '%{}%'".format(text_search))
    common.data_loader(self, self.database, 'None', self.tableWidget_resident, query)

def resident_manage_resident_tab_add_resident(self):
    if self.lineEdit_resident_name.text() and self.lineEdit_resident_id_number.text():
        phone_number = self.lineEdit_resident_phone.text()
        id_number = self.lineEdit_resident_id_number.text()
        if (len(phone_number) > 0 and len(phone_number) <10) or (len(id_number) > 0 and (len(id_number) != 9) and len(id_number)!=12):
            if len(phone_number) > 0 and len(phone_number) <10:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Phone Must Be lenght 10").exec()
            else:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Must Be lenght = 9 or 13").exec()
        else:
            name = self.lineEdit_resident_name.text()
            birthday = self.dateEdit_resident_birthday.date()
            birthday_mysql = standardized.str_date_standard(birthday.year(), birthday.month(), birthday.day())
            gender = self.comboBox_resident_gender.currentText()
            if gender == 'Male':
                gender = 1
            else: gender = 0
            id_number = self.lineEdit_resident_id_number.text()
            phone = phone_number
            village = self.textEdit_resident_village.toPlainText()
            curr_accommodation = self.textEdit_resident_current_accomodation.toPlainText()
            today_mysql = common.get_today_str()
            name_en = common.make_name(name, birthday_mysql, id_number, today_mysql)
            apartment = self.comboBox_resident_room_number.currentData().pk
            query = 'call insert_resident(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor = self.database.cursor()
            try:
                cursor.execute(query,(apartment, name, name_en, birthday_mysql, gender, id_number, phone, village, curr_accommodation))
                self.database.commit()
                common.data_loader(self, self.database, 'None', self.tableWidget_resident, fully_query_resident)
            except db.Error as e:
                print(e)
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Is Exist!").exec()
            cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name or ID Number must be Not Null").exec()

def resident_manage_resident_tab_edit_resident(self):
    if self.lineEdit_resident_id.text():
        cur_id_resident = int(self.lineEdit_resident_id.text())
        if self.lineEdit_resident_name.text() and self.lineEdit_resident_id_number.text():
            phone_number = self.lineEdit_resident_phone.text()
            id_number = self.lineEdit_resident_id_number.text()
            if (len(phone_number) > 0 and len(phone_number) < 10) or (len(id_number) > 0 and (len(id_number) != 9) and len(id_number)!=12):
                if len(phone_number) > 0 and len(phone_number) < 10:
                    message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Phone Must Be lenght 10").exec()
                else:
                    message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Must Be lenght = 9 or 13").exec()
            else:
                query_get_cur_resident = '''
                    select p.id, a.name as 'apartment', a.id as 'apartment_id', p.name, p.birthday, 
                    if(p.gender=1, 'Male', 'Female') as 'gender', p.id_card, 
                    p.phone, p.village, p.current_accommodation  from person as p
                    join resident_apartment as r on p.id = r.resident
                    join apartment as a on a.id = r.apartment
                    join floor as f on a.floor = f.id
                    join building as b on b.id = f.building
                    join type_of_floor as t on t.id = 2
                    where p.is_delete = 0 and p.is_resident = 1 and p.id = {}
                '''
                cur_resident = common.get_single_item_from_query(query_get_cur_resident.format(cur_id_resident), self.database)
                name = self.lineEdit_resident_name.text()
                birthday = self.dateEdit_resident_birthday.date()
                birthday_mysql = standardized.str_date_standard(birthday.year(), birthday.month(), birthday.day())
                gender = self.comboBox_resident_gender.currentText()
                if gender == 'Male':
                    gender = 1
                else: gender = 0
                id_number = self.lineEdit_resident_id_number.text()
                phone =self.lineEdit_resident_phone.text()
                village = self.textEdit_resident_village.toPlainText()
                curr_accommodation = self.textEdit_resident_current_accomodation.toPlainText()
                apartment = self.comboBox_resident_room_number.currentData().pk
                today_mysql = common.get_today_str()
                query = 'call edit_resident(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor = self.database.cursor()
                try:
                    cursor.execute(query,(apartment, name, birthday_mysql, gender, phone, id_number, village, curr_accommodation, cur_resident[6], cur_resident[2]))
                    print(cursor._last_executed)
                    self.database.commit()
                    common.data_loader(self, self.database, 'None', self.tableWidget_resident, fully_query_resident)
                except db.Error as e:
                    print(e)
                    message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Is Exist!").exec()
                cursor.close()
        else:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name or ID Number must be Not Null").exec()

def resident_manage_resident_tab_delete_resident(self):
    if self.lineEdit_resident_id.text():
        cur_id_resident = int(self.lineEdit_resident_id.text())
        common.delete_item(self, 'resident_apartment', self.database, cur_id_resident, self.resident_manage_resident_load, self.resident_manage_resident_tab_clear_form)

def resident_manage_resident_tab_clear_form(self):
    self.lineEdit_resident_id.setText(None)
    self.lineEdit_resident_name.setText(None)
    date_tpm = QDate()
    date_tpm.setDate(2000, 1, 1)
    self.dateEdit_resident_birthday.setDate(date_tpm)
    self.comboBox_resident_gender.setCurrentIndex(0)
    self.lineEdit_resident_id_number.setText(None)
    self.lineEdit_resident_phone.setText(None)
    self.textEdit_resident_village.setPlainText(None)
    self.textEdit_resident_current_accomodation.setPlainText(None)
    self.comboBox_company_staff_building.setCurrentIndex(0)
    self.comboBox_resident_floor.setCurrentIndex(0)
    self.pushButton_import_resident.setEnabled(False)

def resident_manage_resident_tab_select_file_import_resident(self):
    common.select_file_building_setting(self, self.pushButton_select_resident, self.pushButton_import_resident)

def resident_manage_resident_tab_import_file_resident(self):
    file_path = self.pushButton_select_company_staff_file.text()
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
                apartment = row['apartment']
                name = row['name']
                birthday = row['birthday']
                gender = row['gender']
                id_card = str(row['id_card'])
                phone = row['phone']
                village = row['village']
                current_accomodation = row['current_accommodation']
                cur_date = common.get_today_str()
                name_en = common.make_name(name, birthday, id_card, cur_date)
                try:
                    query = "call insert_staff_from_file(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    cursor.execute(query, (apartment, name, name_en ,birthday, gender, phone, id_card, village, current_accomodation))
                    self.database.commit()
                except db.Error as e:
                    print(e)
            cursor.close()
        except:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!").exec()
    self.resident_manage_staff_load()

def resident_manage_resident_tab_export_file_resident(self):
    path_file = common.select_file_export(self, self.pushButton_export_resident)
    if path_file:
        common.export_data_from_table_widget(self, self.tableWidget_resident, path_file)
        self.statusBar().showMessage("Export Success")

def resident_manage_resident_tab_item_click(self):
    data = common.get_row_data_item_click(self.tableWidget_resident)
    self.lineEdit_resident_id.setText(data[0])
    self.lineEdit_resident_name.setText(data[2])
    gender_index = self.comboBox_resident_gender.findText(data[4])
    self.comboBox_resident_gender.setCurrentIndex(gender_index)
    self.lineEdit_resident_id_number.setText(data[5])
    if data[6] != 'None':
        self.lineEdit_resident_phone.setText(data[6])
    else:
        self.lineEdit_resident_phone.setText(None)
    self.textEdit_resident_village.setPlainText(data[7])
    self.textEdit_resident_current_accomodation.setPlainText(data[8])
    if data[3]:
        date_temp = data[3].split('-')
        birthday = QDate()
        birthday.setDate(int(date_temp[0]), int(date_temp[1]), int(date_temp[2]))
        self.dateEdit_resident_birthday.setDate(birthday)

    apartment_name = data[1]

    query_select_apartment_building = '''
        select a.id as 'apartment_id', a.name as 'apartment', f.id as 'floor_id', 
        f.name as 'floor', b.id as 'building_id', b.name as 'building' from apartment as a
        join floor as f on a.floor = f.id
        join building as b on b.id = f.building
        join type_of_floor as t on t.id = f.type_of_floor
        where t.id = 2 and a.name = '{}'
    '''
    list_apartment_building = common.get_list_model(self.database, my_model.Apartment_Floor_Building, query_select_apartment_building.format(apartment_name))
    target = list_apartment_building[0]
    building_index = self.comboBox_resident_building.findText(target[5])
    self.comboBox_resident_building.setCurrentIndex(building_index)

    text_find = 'Tầng {} Tòa Nhà {}'.format(target[3], target[5])
    floor_index = self.comboBox_resident_floor.findText(text_find)
    self.comboBox_resident_floor.setCurrentIndex(floor_index)

    apartment_index = self.comboBox_resident_room_number.findText('Phòng ' + target[1])
    self.comboBox_resident_room_number.setCurrentIndex(apartment_index)


def resident_manage_resident_tab_data_change_floor_combobox(self):
    common.set_floor_combobox_data_change(self.comboBox_resident_building, self.comboBox_resident_floor, 2, self.database)

def resident_manage_resident_tab_data_change_apartment_combobox(self):
    common.set_apartment_combobox_data_change(self.comboBox_resident_building, self.comboBox_resident_floor, self.comboBox_resident_room_number, self.database)

def resident_manage_resident_tab_data_change_building_combobox(self):
    common.set_building_combobox_data_change(self.comboBox_resident_building, self.database)