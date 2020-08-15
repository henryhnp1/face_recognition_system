from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox
import pandas as pd
import os
from PyQt5.QtCore import Qt, QRegExp, QDate
import MySQLdb as db

from util import common, standardized, message_box
from models import my_model


fully_query_grant_role = '''
    select pdp.id, b.name as 'building', f.name as 'floor', d.name as 'door', p.name as 'person',  p.id_card, p.phone, p.current_accommodation, pm.name as 'permission' from person_door_permission as pdp 
    join person as p on pdp.person = p.id
    join door as d on pdp.door = d.id
    join floor as f on d.floor = f.id
    join building as b on f.building = b.id
    join permission as pm on pdp.permission = pm.id
    join role_door as rd on d.role = rd.id
    where rd.id = 2 order by p.name;
'''
def admin_access_control_grant_role_clear_form(self):
    self.pushButton_select_file_grant_role.setText('Choose File')
    self.pushButton_import_grant_role.setEnabled(False)
    self.lineEdit_id_grant_role.setText(None)
    self.lineEdit_id_num_grant_role.setText(None)
    self.textEdit_info_person.setPlainText(None)
    self.comboBox_grant_role_block.setCurrentIndex(0)
    self.comboBox_grant_role_floor.setCurrentIndex(0)
    self.comboBox_grant_role_door.setCurrentIndex(0)
    self.comboBox_grant_role_door_permission.setCurrentIndex(0)

def access_control_grant_role_load(self):
    common.data_loader(self, self.database, '', self.tableWidget_grant_role, fully_query_grant_role)

def access_control_handle_button_grant_role_tab(self):
    self.pushButton_export_grant_role.clicked.connect(self.access_control_grant_role_export)
    self.pushButton_select_file_grant_role.clicked.connect(self.access_control_grant_role_choose_file)
    self.pushButton_import_grant_role.clicked.connect(self.access_control_grant_role_import_file)
    self.pushButton_grant_role_add.clicked.connect(self.access_control_grant_role_add)
    self.pushButton_grant_role_edit.clicked.connect(self.access_control_grant_role_edit)
    self.pushButton_grant_role_delete.clicked.connect(self.access_control_grant_role_delete)

def access_control_handle_combobox_grant_role_tab(self):
    self.comboBox_fields_search_grant_role.currentTextChanged.connect(self.access_control_grant_role_setting_line_search)
    self.comboBox_grant_role_block_search.currentTextChanged.connect(self.access_control_grant_role_combobox_data_change_floor_search)
    self.comboBox_grant_role_floor_search.currentTextChanged.connect(self.access_control_grant_role_combobox_data_change_door_search)
    self.comboBox_grant_role_block.currentTextChanged.connect(self.access_control_grant_role_combobox_data_change_floor)
    self.comboBox_grant_role_floor.currentTextChanged.connect(self.access_control_grant_role_combobox_data_change_door)

def access_control_combobox_setting_grant_role_tab(self):
    field_apartment_search = ['id', 'name', 'id_card', 'phone', 'current accommodation', 'permission']
    self.comboBox_fields_search_grant_role.addItems(field_apartment_search)

def access_control_combobox_setting_data_change_grant_role_tab(self):
    self.access_control_grant_role_combobox_data_change_building_search()
    self.access_control_grant_role_combobox_data_change_building()
    self.access_control_grant_role_combobox_data_change_permission()

def access_control_handle_search_line_edit_grant_role_tab(self):
    self.lineEdit_line_search_grant_role.returnPressed.connect(self.access_control_grant_role_seach)

def access_control_table_widget_setting_grant_role_tab(self):
    self.tableWidget_grant_role.setSortingEnabled(True)
    self.tableWidget_grant_role.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_grant_role.itemClicked.connect(self.access_control_grant_role_item_click)

def access_control_button_setting_and_ui_grant_role_tab(self):
    self.pushButton_select_file_grant_role.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
    self.pushButton_import_grant_role.setEnabled(False)

def access_control_grant_role_setting_line_search(self):
    field_search = self.comboBox_fields_search_grant_role.currentText()
    if field_search == 'id' or field_search=='id_card' or field_search=='phone':
        self.lineEdit_line_search_grant_role.setText('')
        self.lineEdit_line_search_grant_role.setValidator(QRegExpValidator(QRegExp("[0-9]{0,12}")))
    else:
        self.lineEdit_line_search_grant_role.setValidator(None)

def access_control_grant_role_seach(self):
    field_search = self.comboBox_fields_search_grant_role.currentText()
    text_search = self.lineEdit_line_search_grant_role.text()
    building_object = self.comboBox_grant_role_block_search.currentData()
    building_id = ''
    floor_id = ''
    door_id = ''
    if building_object:
        floor_object = self.comboBox_grant_role_floor_search.currentData()
        building_id = building_object.pk
        if floor_object:
            door_object = self.comboBox_grant_role_door_search.currentData()
            floor_id = floor_object.pk
            if door_object:
                door_id = door_object.pk
    query = '''
        select pdp.id, b.name as 'building', f.name as 'floor', d.name as 'door', p.name as 'person',  p.id_card, p.phone, p.current_accommodation, pm.name as 'permission' from person_door_permission as pdp 
        join person as p on pdp.person = p.id
        join door as d on pdp.door = d.id
        join floor as f on d.floor = f.id
        join building as b on f.building = b.id
        join permission as pm on pdp.permission = pm.id
        join role_door as rd on d.role = rd.id
        where rd.id = 2 {}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("and pdp.id like '%{}%'".format(int(text_search)))
    elif field_search == 'name':
        query = query.format("and p.name like '%{}%'".format(text_search))
    elif field_search == 'id card':
        query = query.format("and p.id_card like '%{}%'".format(text_search))
    elif field_search == 'phone':
        query = query.format("and p.phone like '%{}%'".format(text_search))
    elif field_search == 'permission':
        query = query.format("and pm.name like '%{}%'".format(text_search))
    else:
        query = query.format("and p.current_accommodation like '%{}%'".format(text_search))
    
    if door_id:
        query = query + ' and d.id = {} and f.id = {} and b.id = {}'.format(door_id, floor_id, building_id)
    elif floor_id:
        query = query + ' and f.id = {} and b.id = {}'.format(floor_id, building_id)
    elif building_id:
        query = query + ' and b.id = {}'.format(building_id)
    else:
        query = query
    
    common.data_loader_without_change_combobox(self, self.database, 'None', self.tableWidget_grant_role, query)

def access_control_grant_role_item_click(self):
    data = common.get_row_data_item_click(self.tableWidget_grant_role)
    self.lineEdit_id_grant_role.setText(data[0])
    self.lineEdit_id_num_grant_role.setText(data[5])
    info = 'Name: '+data[4]+'\nPhone: '+(data[6] if data[6]!='None' else '')+'\nAccommodation: '+data[7]
    self.textEdit_info_person.setPlainText(info)

    building_index = self.comboBox_grant_role_block.findText(data[1])
    self.comboBox_grant_role_block.setCurrentIndex(building_index)

    text_find_floor = 'Tầng {} Tòa Nhà {}'.format(data[2], data[1])
    floor_index = self.comboBox_grant_role_floor.findText(text_find_floor)
    self.comboBox_grant_role_floor.setCurrentIndex(floor_index)

    text_find_door = 'Cửa {}'.format(data[3])
    door_index = self.comboBox_grant_role_door.findText(text_find_door)
    self.comboBox_grant_role_door.setCurrentIndex(door_index)

    permission_index = self.comboBox_grant_role_door_permission.findText(data[8])
    self.comboBox_grant_role_door_permission.setCurrentIndex(permission_index)


def access_control_grant_role_export(self):
    if self.tableWidget_grant_role.rowCount():
        path_file = common.select_file_export(self, self.pushButton_export_grant_role)
        if path_file:
            common.export_data_from_table_widget(self, self.tableWidget_grant_role, path_file)
            self.statusBar().showMessage("Export Success")
    else:
        message_box.MyMessageBox(QMessageBox.Critical, 'Error', 'No data to export')

def access_control_grant_role_choose_file(self):
    common.select_file_building_setting(self, self.pushButton_select_file_grant_role, self.pushButton_import_grant_role)

def access_control_grant_role_import_file(self):
    file_path = self.pushButton_select_file_grant_role.text()
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
                floor = row['floor']
                door = row['door']
                id_card = str(row['id_card'])
                permisson = row['permission']
                try:
                    query = "call insert_grant_role_from_file(%s, %s, %s, %s, %s);"
                    cursor.execute(query, (building, floor, door, id_card, permission))
                    self.database.commit()
                except db.Error as e:
                    print(e)
            cursor.close()
        except:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!").exec()
    self.resident_manage_staff_load()

def access_control_grant_role_add(self):
    if self.lineEdit_id_num_grant_role.text():
        id_num = self.lineEdit_id_num_grant_role.text()
        door_object = self.comboBox_grant_role_door.currentData()
        permission_object = self.comboBox_grant_role_door_permission.currentData()

        if door_object and permission_object:
            person_id = common.get_single_value_from_table('person', 'id', "where id_card = '{}'".format(id_num), self.database)
            if person_id:
                query = 'insert into person_door_permission(person, door, permission) value (%s, %s, %s)'
                cursor = self.database.cursor()
                try:
                    cursor.execute(query,(person_id, door_object.pk, permission_object.pk))
                    self.database.commit()
                    common.data_loader_without_change_combobox(self, self.database, 'None', self.tableWidget_grant_role, fully_query_grant_role)
                except db.Error as e:
                    message_box.MyMessageBox(QMessageBox.Critical, "Error","Role is existed!")
                cursor.close()
            else:
                message_box.MyMessageBox(QMessageBox.Critical, "Error","Person is not exist")
        else:
            message_box.MyMessageBox(QMessageBox.Critical, "Error","Please grant role for person in door")
    else:
        pass

def access_control_grant_role_edit(self):
    if self.lineEdit_id_grant_role.text():
        id_grant_role = int(self.lineEdit_id_grant_role.text())
        id_card = self.lineEdit_id_num_grant_role.text()
        if id_grant_role and id_card:
            door_object = self.comboBox_grant_role_door.currentData()
            permission_object = self.comboBox_grant_role_door_permission.currentData()
            person_id = common.get_single_value_from_table('person', 'id', "where id_card = '{}'".format(id_card), self.database)
            if door_object and permission_object:
                query = 'update person_door_permission set door = %s, permission = %s where id = %s'
                cursor = self.database.cursor()
                try:
                    cursor.execute(query, (door_object.pk, permission_object.pk, id_grant_role))
                    self.database.commit()
                    common.data_loader_without_change_combobox(self, self.database, 'None', self.tableWidget_grant_role, fully_query_grant_role)
                except db.Error as e:
                    message_box.MyMessageBox(QMessageBox.Critical, 'Error', 'This person has same role exist')
        else:
            message_box.MyMessageBox(QMessageBox.Critical, 'No Data', 'Plese choose one before edit')
    else:
        pass

def access_control_grant_role_delete(self):
    if self.lineEdit_id_grant_role.text():
        id_grant_role = int(self.lineEdit_id_grant_role.text())
        common.delete_item(self, 'person_door_permission', self.database, id_grant_role, self.access_control_grant_role_load, self.access_control_grant_role_setting_form)

def access_control_grant_role_setting_form(self):
    self.lineEdit_id_grant_role.setText('')
    self.lineEdit_id_num_grant_role.setText('')
    self.textEdit_info_person.setPlainText('')

    self.access_control_combobox_setting_data_change_grant_role_tab()
    common.setting_clear_ui_select_and_import_file(self.pushButton_select_file_grant_role, self.pushButton_import_grant_role)

def access_control_grant_role_combobox_data_change_building_search(self):
    common.set_building_combobox_data_change_search(self.comboBox_grant_role_block_search, self.database)

def access_control_grant_role_combobox_data_change_floor_search(self):
    common.set_floor_combobox_data_change_search(self.comboBox_grant_role_block_search, self.comboBox_grant_role_floor_search,None, self.database)

def access_control_grant_role_combobox_data_change_door_search(self):
    common.set_door_combobox_data_change_search(self.comboBox_grant_role_block_search, self.comboBox_grant_role_floor_search, self.comboBox_grant_role_door_search, self.database)

def access_control_grant_role_combobox_data_change_building(self):
    common.set_building_combobox_data_change(self.comboBox_grant_role_block, self.database)

def access_control_grant_role_combobox_data_change_floor(self):
    common.set_floor_combobox_data_change(self.comboBox_grant_role_block, self.comboBox_grant_role_floor, None, self.database)

def access_control_grant_role_combobox_data_change_door(self):
    common.set_door_combobox_data_change(self.comboBox_grant_role_block, self.comboBox_grant_role_floor, self.comboBox_grant_role_door, self.database)

def access_control_grant_role_combobox_data_change_permission(self):
    common.set_permisson_door_combobox_data_change(self.comboBox_grant_role_door_permission, self.database)

