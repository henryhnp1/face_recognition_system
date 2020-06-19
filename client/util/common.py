from PyQt5.QtWidgets import *
from .message_box import MyMessageBox
from .standardized import str_standard
import pandas as pd
import os
import MySQLdb as db

def search_common_building_setting(option_search, line_search, table, loader):
    field_search = option_search.currentText()
    text_search = line_search.text()
    if field_search == 'id':
        query = 'select * from {} where {}={}'.format(table, field_search, int(text_search))
    else:
        if text_search == None or text_search == '':
            query = 'select * from {}'.format(table)
        query = 'select * from {} where {} like {}'.format(table, field_search, "'%"+text_search+"%'")
    loader(query)

def select_file_building_setting(parent, button_select_file, button_import_file):
    file_path = QFileDialog.getOpenFileName(parent, 'Select File', '/home',"Excel(*.csv *.xlsx)")
    button_select_file.setText(file_path[0])
    if button_select_file.text():
        button_import_file.setEnabled(True)

def import_file_building_setting(button_select_file, database_connection, table, loader):
    file_path = button_select_file.text()
    filename, file_extension = os.path.splitext(file_path)
    with open(file_path, mode='rb') as f:
        if file_extension == '.csv':
            reader = pd.read_csv(f)
        else:
            reader = pd.read_excel(f)
        header = reader.columns
        cursor = database_connection.cursor()
        try:
            for index, row in reader.iterrows():
                name = str_standard(str(row['name']))
                description = str_standard(str(row['description']))
                try:
                    query = "insert into {}(name, description) ".format(table)
                    cursor.execute(query+  "value(%s, %s)", (name, description))
                    database_connection.commit()
                except db.Error as e:
                    print(e)
            cursor.close()
        except:
            MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!").exec()
    loader()

def set_push_button_when_other_clicked(*args):
    for arg in args:
        arg.setStyleSheet("QPushButton{}")

def set_current_tab_active(tab):
    tab.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; background-color: green; color: white}")

def set_tab_when_clicked(tab, *args):
    set_push_button_when_other_clicked(*args)
    set_current_tab_active(tab)

def data_loader(parent, database, table, table_data, query=None):
    if query == None:
        query = "select * from {}".format(table)
    cursor = database.cursor()
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        field_names = [x[0] for x in cursor.description]  #get headname
        table_data.setRowCount(0)
        table_data.setHorizontalHeaderLabels(field_names)  #set headname
        for row_index, row_data in enumerate(data):
            table_data.insertRow(row_index)
            for column, item in enumerate(row_data):
                table_data.setItem(row_index, column, QTableWidgetItem(str(item)))
        cursor.close()
        parent.combobox_setting_data_change()
    except:
        pass

def delete_item(parent, table, database, index, loader, setting_form):
    cursor = database.cursor()
    try:
        query = "delete from {} ".format(table)
        cursor.execute(query + "where id=%s", [(index)])
        database.commit()
        loader()
        parent.statusBar().showMessage("A {} Deleted With ID={}".format(table, index))
        setting_form()
        cursor.close()
    except db.Error as e:
        pass