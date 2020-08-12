from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QTableView, QMessageBox
import pandas as pd
import os
import MySQLdb as db

from util import common, standardized, message_box
from models import my_model

fully_query = "select f.id, f.name, b.name as 'building', t.name as 'type of floor', f.number_of_apartment as 'number apartments' from floor as f, building as b, type_of_floor as t where f.building = b.id and f.type_of_floor = t.id order by b.name, f.id, t.name"

def building_manage_floor_manage_load(self, query=None):
    query = "select f.id, f.name, b.name as 'building', t.name as 'type of floor', f.number_of_apartment as 'number apartments' from floor as f, building as b, type_of_floor as t where f.building = b.id and f.type_of_floor = t.id order by b.name, f.id, t.name"
    common.data_loader(self, self.database, 'floor', self.tableWidget_floor, query)

def building_manage_handle_button_floor_manage_tab(self):
    self.pushButton_add_floor.clicked.connect(self.building_manage_floor_manage_add_floor)
    self.pushButton_edit_floor.clicked.connect(self.building_manage_floor_manage_edit_floor)
    self.pushButton_delete_floor.clicked.connect(self.building_manage_floor_manage_delete_floor)
    self.pushButton_choose_import_file_floor.clicked.connect(self.building_manage_floor_manage_select_file_import_floor)
    self.pushButton_import_floor_file.clicked.connect(self.building_manage_floor_manage_import_file_floor)

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
    for building in data_building:
        building_object = my_model.Building(building[0], building[1], building[2], building[3], building[4])
        self.comboBox_floor_building.addItem(building_object.name, building_object)
    
    cursor.execute(query_select_type_of_floor)
    data_type_of_floor = cursor.fetchall()
    for type_of_floor in data_type_of_floor:
        tfl_object = my_model.TypeOfFloor(type_of_floor[0], type_of_floor[1], type_of_floor[2])
        self.comboBox_typeOfFloor.addItem(tfl_object.name, tfl_object)

def building_manage_floor_manage_tab_table_widget_setting(self):
    self.tableWidget_floor.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_floor.itemClicked.connect(self.building_manage_floor_manage_floor_item_click)
    self.tableWidget_floor.setSortingEnabled(True)

def building_manage_button_setting_and_ui_floor_tab(self):
    self.pushButton_choose_import_file_floor.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")

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
    if self.spinBox_name_floor.value() > 0:
        name = self.spinBox_name_floor.value()
        building = self.comboBox_floor_building.currentData().pk
        type_of_floor = self.comboBox_typeOfFloor.currentData().pk
        number_of_apartment = self.spinBox_numOfApartment.value()

        query = 'insert into floor(name, building, type_of_floor, number_of_apartment) value (%s, %s, %s, %s)'
        cursor = self.database.cursor()
        try:
            cursor.execute(query,(name, building, type_of_floor, number_of_apartment))
            self.database.commit()
            common.data_loader(self, self.database, 'floor', self.tableWidget_floor, fully_query)
        except db.Error as e:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Floor Is Exist!").exec()
        cursor.close()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of floor must be bigger than 0").exec()

def building_manage_floor_manage_edit_floor(self):
    if self.lineEdit_id_floor.text():
        index = int(self.lineEdit_id_floor.text())
        if self.spinBox_name_floor.value() > 0:
            name = self.spinBox_name_floor.value()
            building = self.comboBox_floor_building.currentData().pk
            type_of_floor = self.comboBox_typeOfFloor.currentData().pk
            number_of_apartment = self.spinBox_numOfApartment.value()
            query = 'update floor set name=%s, building=%s, type_of_floor=%s, number_of_apartment=%s where id=%s'
            cursor = self.database.cursor()
            try:
                cursor.execute(query,(name, building, type_of_floor, number_of_apartment, index))
                self.database.commit()
                common.data_loader(self, self.database, 'floor', self.tableWidget_floor, fully_query)
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "The Floor Is Exist!").exec()
            cursor.close()
        else:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "The name of floor must be number bigger than 0").exec()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, "Error", "No Data!").exec()


def building_manage_floor_manage_delete_floor(self):
    if self.lineEdit_id_floor.text():
        index = int(self.lineEdit_id_floor.text())
        common.delete_item(self, 'floor', self.database, index, self.building_manage_floor_manage_load, self.building_manage_floor_manage_clear_form)
    else:
       message_box.MyMessageBox(QMessageBox.Critical, "Error", "No Data!").exec()

def building_manage_floor_manage_select_file_import_floor(self):
    common.select_file_building_setting(self, self.pushButton_choose_import_file_floor, self.pushButton_import_floor_file)

def building_manage_floor_manage_import_file_floor(self):
    file_path = self.pushButton_choose_import_file_floor.text()
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
                name = int(row['name'])
                building = int(row['building'])
                type_of_floor = int(row['type_of_floor'])
                number_of_apartment = int(row['number_of_apartment'])
                try:
                    query = "insert into floor(name, building, type_of_floor, number_of_apartment) "
                    cursor.execute(query+  "value(%s, %s, %s, %s);", (name, building, type_of_floor, number_of_apartment))
                    print(cursor._last_executed )
                    self.database.commit()
                except db.Error as e:
                    print(e)
            cursor.close()
        except:
            message_box.MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!").exec()
    self.building_manage_floor_manage_load()

def building_manage_floor_manage_floor_item_click(self):
    current_row = self.tableWidget_floor.currentRow()
    columns_num = self.tableWidget_floor.columnCount()
    data = []
    for cell in range(0, columns_num):
        item = self.tableWidget_floor.item(current_row, cell).text()
        data.append(item)

    self.lineEdit_id_floor.setText(data[0])
    self.spinBox_name_floor.setValue(int(data[1]))

    query = "select * from building"
    list_model = common.get_list_model(self.database, my_model.Building, query)
    self.spinBox_numOfApartment.setValue(int(data[4]))

    for i, model in enumerate(list_model):
        if data[2] == model[1]:
            self.comboBox_floor_building.setCurrentIndex(i)
            break
    
    # todo change how to don't need query
    query1 = "select * from type_of_floor"
    list_tfl = common.get_list_model(self.database, my_model.TypeOfFloor, query1)
    for i, model in enumerate(list_tfl):
        if data[3] == model[1]:
            self.comboBox_typeOfFloor.setCurrentIndex(i)
            break


def building_manage_floor_manage_combobox_building_selected(self, index):
    itemName = self.comboBox_floor_building.currentText()
    building_object = self.comboBox_floor_building.itemData(index)

def building_manage_floor_manage_clear_form(self):
    self.lineEdit_id_floor.setText(None)
    self.spinBox_name_floor.setValue(0)
    self.comboBox_floor_building.setCurrentIndex(0)
    self.comboBox_typeOfFloor.setCurrentIndex(0)
    self.spinBox_numOfApartment.setValue(0)
    self.pushButton_choose_import_file_floor.setText("Choose File")
    self.pushButton_import_floor_file.setEnabled(False)