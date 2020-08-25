from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox
import pandas as pd
import os
from PyQt5.QtCore import Qt, QRegExp, QDate
import MySQLdb as db

from util import common, standardized, message_box
from models import my_model

fully_select_guest_visit = '''
    select oiog.id, p.name, p.birthday, if(p.gender=1, 'Male', 'Female') as 'gender', p.id_card, p.phone, p.village, 
    p.current_accommodation, a.name as 'apartment', oiog.time_in, oiog.time_out,
    if (oiog.visit_to=1,'bussiness','resident') as 'visit to' from guest as g 
    join person as p on p.id = g.person
    join out_in_of_guest as oiog on oiog.guest = g.id
    join apartment as a on a.id = oiog.apartment;
'''

def security_guest_guest_visit_clear_form(self):
    self.comboBox_fields_search_guest_visit.setCurrentIndex(0)
    self.lineEdit_search_guest_visit.setText(None)
    self.lineEdit_guest_visit_id.setText(None)
    self.lineEdit_guest_visit_name.setText(None)
    self.comboBox_guest_gender.setCurrentIndex(0)
    self.lineEdit_guest_id_number.setText(None)
    self.lineEdit_guest_phone.setText(None)
    self.textEdit_guest_resident_village.setPlainText(None)
    self.textEdit_guest_current_accomodation.setPlainText(None)
    self.comboBox_guest_target_visit.setCurrentIndex(0)
    self.comboBox_guest_target_visit_resident_block.setCurrentIndex(0)
    self.comboBox_guest_target_visit_bussiness_block.setCurrentIndex(0)

def security_guest_guest_visit_load(self):
    common.data_loader(self, self.database, None, self.tableWidget_guest_visit, fully_select_guest_visit)

def security_guest_handle_button_guest_visit_tab(self):
    self.pushButton_export_guest_visit.clicked.connect(self.security_guest_guest_visit_export_guest_visit)
    self.pushButton_guest_visit_add.clicked.connect(self.security_guest_guest_visit_add_guest_visit)
    self.pushButton_guest_visit_edit.clicked.connect(self.security_guest_guest_visit_edit_guest_visit)
    self.pushButton_guest_visit_delete.clicked.connect(self.security_guest_guest_visit_delete_guest_visit)
def security_guest_handle_combobox_guest_visit_tab(self):
    self.comboBox_fields_search_guest_visit.currentTextChanged.connect(self.security_guest_guest_visit_tab_setting_line_search)
    self.comboBox_guest_target_visit.currentTextChanged.connect(self.security_guest_guest_visit_setting_target_visit)
    self.comboBox_guest_target_visit_bussiness_block.currentTextChanged.connect(self.security_guest_visit_bussiness_data_change_floor_combobox)
    self.comboBox_guest_target_visit_bussiness_floor.currentTextChanged.connect(self.security_guest_visit_bussiness_data_change_company_combobox)
    self.comboBox_guest_target_visit_resident_block.currentTextChanged.connect(self.security_guest_visit_resident_data_change_floor_combobox)
    self.comboBox_guest_target_visit_resident_floor.currentTextChanged.connect(self.security_guest_visit_resident_data_change_apartment_combobox)

def security_guest_combobox_setting_guest_visit_tab(self):
    field_search_visit = ['id', 'name', 'gender', 'id card', 'phone', 'village', 'apartment', 'visit to']
    self.comboBox_fields_search_guest_visit.addItems(field_search_visit)

    field_gender = ['Male', 'Female']
    self.comboBox_guest_gender.addItems(field_gender)

    field_visit_to = ['bussiness', 'resident']
    self.comboBox_guest_target_visit.addItems(field_visit_to)

def security_guest_combobox_setting_data_change_guest_visit_tab(self):
    self.security_guest_visit_bussiness_data_change_building_combobox()
    self.security_guest_visit_resident_data_change_building_combobox()

def security_guest_handle_search_line_edit_guest_visit_tab(self):
    self.lineEdit_search_guest_visit.returnPressed.connect(self.security_guest_guest_visit_search)

def security_guest_table_widget_setting_guest_visit_tab(self):
    self.tableWidget_guest_visit.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_guest_visit.itemClicked.connect(self.security_guest_guest_visit_item_click)

def security_guest_button_setting_and_ui_guest_visit_tab(self):
    self.tabWidget_guest_target_visit.tabBar().setVisible(False)
    self.lineEdit_guest_id_number.setValidator(QRegExpValidator(QRegExp("[0-9]{9,12}")))
    self.lineEdit_guest_phone.setValidator(QRegExpValidator(QRegExp("[0-9]{10}")))


def security_guest_guest_visit_tab_setting_line_search(self):
    field_search = self.comboBox_fields_search_guest_visit.currentText()
    if field_search == 'id' or field_search=='id card' or field_search == 'phone':
        self.lineEdit_search_guest_visit.setText('')
        self.lineEdit_search_guest_visit.setValidator(QRegExpValidator(QRegExp("[0-9]{9,12}")))
    else:
        self.lineEdit_search_guest_visit.setValidator(None)

def security_guest_guest_visit_item_click(self):
    data = common.get_row_data_item_click(self.tableWidget_guest_visit)
    if data:
        guest_visit = my_model.GuestVisit(*data)
        self.lineEdit_guest_visit_id.setText(guest_visit.pk)
        self.lineEdit_guest_visit_name.setText(guest_visit.name)
        self.lineEdit_guest_id_number.setText(guest_visit.id_card)
        self.lineEdit_guest_phone.setText(guest_visit.phone if guest_visit.phone !='None' else '')
        self.textEdit_guest_resident_village.setPlainText(guest_visit.village)
        self.textEdit_guest_current_accomodation.setPlainText(guest_visit.accommodation)
        
        gender_index = self.comboBox_guest_gender.findText(guest_visit.gender)
        self.comboBox_guest_gender.setCurrentIndex(gender_index)

        visit_to_index = self.comboBox_guest_target_visit.findText(guest_visit.visit_to)
        self.comboBox_guest_target_visit.setCurrentIndex(visit_to_index)

        birthday = common.get_date_from_date_data(guest_visit.birthday)
        self.dateEdit_guest_visit_birthday.setDate(birthday)

        query_select_apartment_building = '''
            select a.id as 'apartment_id', a.name as 'apartment', f.id as 'floor_id', 
            f.name as 'floor', b.id as 'building_id', b.name as 'building' from apartment as a
            join floor as f on a.floor = f.id
            join building as b on b.id = f.building
            join type_of_floor as t on t.id = f.type_of_floor
            where t.id = {} and a.name = '{}' limit 1;
        '''

        if guest_visit.visit_to == 'bussiness':
            self.dateTimeEdit_guest_visit_company_from_time.setDateTime(common.get_datetime_from_datetime_data(guest_visit.time_in))
            self.dateTimeEdit_guest_visit_company_to_time.setDateTime(common.get_datetime_from_datetime_data(guest_visit.time_out))

            apartment_building = common.get_single_item_from_query(query_select_apartment_building.format(1, guest_visit.apartment), self.database)
            target = my_model.Apartment_Floor_Building(*apartment_building)

            building_index = self.comboBox_guest_target_visit_resident_block.findText(target.building_name)
            self.comboBox_guest_target_visit_resident_block.setCurrentIndex(building_index)

            text_find_floor = 'Tầng {} Tòa Nhà {}'.format(target.floor_name, target.building_name)
            floor_index = self.comboBox_guest_target_visit_bussiness_floor.findText(text_find_floor)
            self.comboBox_guest_target_visit_bussiness_floor.setCurrentIndex(floor_index)

            query_get_company_name_from_apartment = '''
                select c.name from company as c join apartment as a
                where c.apartment = a.id and a.name = '{}'; 
            '''
            company_name = common.get_single_value_from_query(query_get_company_name_from_apartment.format(guest_visit.apartment), self.database)
            if company_name:
                text_find_office = 'Công Ty ' + company_name + ' Phòng ' + target.name
                apartment_index = self.comboBox_guest_visit_company.findText(text_find_office)
                self.comboBox_guest_visit_company.setCurrentIndex(apartment_index)
        else:
            self.dateTimeEdit_guest_visit_resident_from_time.setDateTime(common.get_datetime_from_datetime_data(guest_visit.time_in))
            self.dateTimeEdit_guest_visit_resident_to_time.setDateTime(common.get_datetime_from_datetime_data(guest_visit.time_out))

            apartment_building = common.get_single_item_from_query(query_select_apartment_building.format(2, guest_visit.apartment), self.database)
            target = my_model.Apartment_Floor_Building(*apartment_building)

            building_index = self.comboBox_guest_target_visit_resident_block.findText(target.building_name)
            self.comboBox_guest_target_visit_resident_block.setCurrentIndex(building_index)

            text_find_floor = 'Tầng {} Tòa Nhà {}'.format(target.floor_name, target.building_name)
            floor_index = self.comboBox_guest_target_visit_resident_floor.findText(text_find_floor)
            self.comboBox_guest_target_visit_resident_floor.setCurrentIndex(floor_index)

            apartment_index = self.comboBox_guest_visit_appartment.findText('Phòng ' + target.name)
            self.comboBox_guest_visit_appartment.setCurrentIndex(apartment_index)

        
def security_guest_visit_bussiness_data_change_building_combobox(self):
    common.set_building_combobox_data_change(self.comboBox_guest_target_visit_bussiness_block, self.database)

def security_guest_visit_resident_data_change_building_combobox(self):
    common.set_building_combobox_data_change(self.comboBox_guest_target_visit_resident_block, self.database)

def security_guest_visit_bussiness_data_change_floor_combobox(self):
    common.set_floor_combobox_data_change(self.comboBox_guest_target_visit_bussiness_block, self.comboBox_guest_target_visit_bussiness_floor,1, self.database)

def security_guest_visit_resident_data_change_floor_combobox(self):
    common.set_floor_combobox_data_change(self.comboBox_guest_target_visit_bussiness_block, self.comboBox_guest_target_visit_resident_floor,2, self.database) 

def security_guest_visit_bussiness_data_change_company_combobox(self):
    common.set_company_office_combobox_data_change(self.comboBox_guest_target_visit_bussiness_block,
     self.comboBox_guest_target_visit_bussiness_floor,self.comboBox_guest_visit_company, self.database)

def security_guest_visit_resident_data_change_apartment_combobox(self):
    common.set_apartment_combobox_data_change(self.comboBox_guest_target_visit_bussiness_block,
     self.comboBox_guest_target_visit_resident_floor,self.comboBox_guest_visit_appartment, self.database) 


def security_guest_guest_visit_search(self):
    field_search = self.comboBox_fields_search_guest_visit.currentText()
    text_search = self.lineEdit_search_guest_visit.text()
    query = '''
        select oiog.id, p.name, p.birthday, if(p.gender=1, 'Male', 'Female') as 'gender', p.id_card, p.phone, p.village, 
        p.current_accommodation, a.name as 'apartment', oiog.time_in, oiog.time_out,
        if (oiog.visit_to=1,'bussiness','resident') as 'visit to' from guest as g 
        join person as p on p.id = g.person
        join out_in_of_guest as oiog on oiog.guest = g.id
        join apartment as a on a.id = oiog.apartment
        {}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("where oiog.id like '%{}%'".format(int(text_search)))
    elif field_search == 'apartment':
        query = query.format("where a.name like '%{}%'".format(text_search))
    elif field_search == 'name':
        query = query.format("where p.name like '%{}%'".format(text_search))
    elif field_search == 'id card':
        query = query.format("where p.id_card like '%{}%'".format(text_search))
    elif field_search == 'gender':
        if text_search == 'male':
            query = query.format("where p.gender = 1")
        elif text_search == 'female':
            query = query.format("where p.gender = 0")
        else:
            query = query.format('')
    elif field_search == 'visit to':
        if text_search == 'bussiness':
            query = query.format("where oiog.visit_to = 1")
        elif text_search == 'resident':
            query = query.format("where where oiog.visit_to = 2")
        else:
            query = query.format('')
    elif field_search == 'phone':
        query = query.format("where p.phone like '%{}%'".format(text_search))
    elif field_search == 'village':
        query = query.format("where p.village like '%{}%'".format(text_search))
    common.data_loader(self, self.database, 'None', self.tableWidget_guest_visit, query)

def security_guest_guest_visit_setting_target_visit(self):
    index_target_visit = self.comboBox_guest_target_visit.currentIndex()
    self.tabWidget_guest_target_visit.setCurrentIndex(index_target_visit)

def security_guest_guest_visit_add_guest_visit(self):
    if self.lineEdit_guest_visit_name.text() and self.lineEdit_guest_id_number.text():
        phone_number = self.lineEdit_guest_phone.text()
        id_number = self.lineEdit_guest_id_number.text()
        if (len(phone_number) > 0 and len(phone_number) <10) or (len(id_number) > 0 and (len(id_number) != 9) and len(id_number)!=12):
            if len(phone_number) > 0 and len(phone_number) <10:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Phone Must Be lenght 10").exec()
            else:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Must Be lenght = 9 or 13").exec()
        else:
            name = self.lineEdit_guest_visit_name.text()
            birthday = self.dateEdit_guest_visit_birthday.date()
            birthday_mysql = standardized.str_date_standard(birthday.year(), birthday.month(), birthday.day())

            gender = self.comboBox_guest_gender.currentText()
            if gender == 'Male': gender = 1
            else: gender = 0

            visit_to = self.comboBox_guest_target_visit.currentText()
            if visit_to == 'bussiness':visit_to = 1
            else: visit_to = 2

            id_number = self.lineEdit_guest_id_number.text()
            phone = phone_number
            village = self.textEdit_guest_resident_village.toPlainText()
            curr_accommodation = self.textEdit_guest_current_accomodation.toPlainText()
            today_mysql = common.get_today_str()
            name_en = common.make_name(name, birthday_mysql, id_number, today_mysql)
            if visit_to == 1:
                apartment = self.comboBox_guest_visit_company.currentData().pk
                time_in = common.get_mysql_datetime_from_datetime_edit(self.dateTimeEdit_guest_visit_company_from_time)
                time_out = common.get_mysql_datetime_from_datetime_edit(self.dateTimeEdit_guest_visit_company_to_time)
            else:
                apartment = self.comboBox_guest_visit_appartment.currentData().pk
                time_in = common.get_mysql_datetime_from_datetime_edit(self.dateTimeEdit_guest_visit_resident_from_time)
                time_out = common.get_mysql_datetime_from_datetime_edit(self.dateTimeEdit_guest_visit_resident_to_time)
            if apartment == None:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "Choose the location to visit").exec()
            elif time_out < time_in:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "Choose the time go out bigger than time go in").exec()
            else:
                query = "call insert_guest_visit('{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', {}, {}, '{}', '{}')"
                query = query.format(name, name_en, birthday_mysql, id_number, gender, phone, village, curr_accommodation, visit_to, apartment, time_in, time_out)
                cursor = self.database.cursor()
                try:
                    cursor.execute(query)
                    self.database.commit()
                    common.data_loader(self, self.database, 'None', self.tableWidget_guest_visit, fully_select_guest_visit)
                except db.Error as e:
                    print(e)
                    message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Or Phone Is Exist!").exec()
                cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name or ID Number must be Not Null").exec()

def security_guest_guest_visit_edit_guest_visit(self):
    id_out_in = self.lineEdit_guest_visit_id.text()
    if id_out_in:
        id_out_in = int(id_out_in)
        query_get_current_id_card = '''
            select p.id_card from person as p join guest as g on p.id = g.person
            join out_in_of_guest as oiog on oiog.guest = g.id
            where oiog.id = {} limit 1;
        '''
        cur_id_card = common.get_single_value_from_query(query_get_current_id_card.format(id_out_in), self.database)
        if self.lineEdit_guest_visit_name.text() and self.lineEdit_guest_id_number.text():
            phone_number = self.lineEdit_guest_phone.text()
            id_number = self.lineEdit_guest_id_number.text()
            if (len(phone_number) > 0 and len(phone_number) <10) or (len(id_number) > 0 and (len(id_number) != 9) and len(id_number)!=12):
                if len(phone_number) > 0 and len(phone_number) <10:
                    message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Phone Must Be lenght 10").exec()
                else:
                    message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number Must Be lenght = 9 or 13").exec()
            else:
                name = self.lineEdit_guest_visit_name.text()
                birthday = self.dateEdit_guest_visit_birthday.date()
                birthday_mysql = standardized.str_date_standard(birthday.year(), birthday.month(), birthday.day())

                gender = self.comboBox_guest_gender.currentText()
                if gender == 'Male': gender = 1
                else: gender = 0

                visit_to = self.comboBox_guest_target_visit.currentText()
                if visit_to == 'bussiness':visit_to = 1
                else: visit_to = 2

                id_number = self.lineEdit_guest_id_number.text()
                phone = phone_number
                village = self.textEdit_guest_resident_village.toPlainText()
                curr_accommodation = self.textEdit_guest_current_accomodation.toPlainText()
                today_mysql = common.get_today_str()
                if visit_to == 1:
                    apartment = self.comboBox_guest_visit_company.currentData().pk
                    time_in = common.get_mysql_datetime_from_datetime_edit(self.dateTimeEdit_guest_visit_company_from_time)
                    time_out = common.get_mysql_datetime_from_datetime_edit(self.dateTimeEdit_guest_visit_company_to_time)
                else:
                    apartment = self.comboBox_guest_visit_appartment.currentData().pk
                    time_in = common.get_mysql_datetime_from_datetime_edit(self.dateTimeEdit_guest_visit_resident_from_time)
                    time_out = common.get_mysql_datetime_from_datetime_edit(self.dateTimeEdit_guest_visit_resident_to_time)
                if apartment == None:
                    message_box.MyMessageBox(QMessageBox.Critical, "Error", "Choose the location to visit").exec()
                elif time_out < time_in:
                    message_box.MyMessageBox(QMessageBox.Critical, "Error", "Choose the time go out bigger than time go in").exec()
                else:
                    query = 'call edit_guest_visit(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    cursor = self.database.cursor()
                    try:
                        cursor.execute(query,(cur_id_card, name, birthday_mysql, id_number, gender, phone, village, curr_accommodation, id_out_in, visit_to, apartment, time_in, time_out))
                        self.database.commit()
                        common.data_loader(self, self.database, 'None', self.tableWidget_guest_visit, fully_select_guest_visit)
                    except db.Error as e:
                        print(e)
                        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The ID Number or Phone Is Exist!").exec()
                    cursor.close()
        else:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name or ID Number must be Not Null").exec()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "Can not change, please choose one item in table").exec()

def security_guest_guest_visit_delete_guest_visit(self):
    id_out_in = self.lineEdit_guest_visit_id.text()
    if id_out_in:
        id_out_in = int(id_out_in)
        common.delete_item(self, 'out_in_of_guest', self.database, id_out_in, self.security_guest_guest_visit_load, self.security_guest_guest_visit_clear_form)

def security_guest_guest_visit_export_guest_visit(self):
    path_file = common.select_file_export(self, self.pushButton_export_guest_visit)
    if path_file:
        common.export_data_from_table_widget(self, self.tableWidget_guest_visit, path_file)
        self.statusBar().showMessage("Export Success")

