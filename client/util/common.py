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
        # except:
        #     MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!").exec()
    loader()