from PyQt5.QtWidgets import *
from .message_box import MyMessageBox
from .standardized import str_standard
import pandas as pd
import os
import MySQLdb as db
import re
import unicodedata

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

def get_list_model(database, model, query):
    list_model = []
    try:
        cursor = database.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        for item in data:
            # temp_model = model(*item)
            list_model.append(item)
    except db.Error as e:
        print(e)
    return list_model

def make_dir(name_dir):
    try:
        os.mkdir(dir_name)
    except OSError:
        pass

def no_accent_vietnamese(s):
    s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(u'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(u'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(u'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(u'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(u'[ìíịỉĩ]', 'i', s)
    s = re.sub(u'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(u'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(u'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(u'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(u'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    return s

def make_acronym_name(name:str):
    words = name.split()
    if len(words) > 2:
        main_name = words[-1]
        firstname = words[0]
        lastname = words[-2]
        return main_name + firstname[0] + lastname[0]
    else:
        return words[1] + words[0]

def make_name(name, birthday, id_num, current_date):
    name = make_acronym_name(name).upper()
    birthdays = birthday.split('-')
    birthday = birthdays[1] + birthdays[2]
    id_num = id_num[-3:]
    current_dates = current_date.split('-')
    current_date = current_dates[2] + '_' + current_dates[1] + '_' + current_dates[0][-2:]
    return '{}_{}_{}'.format(name+birthday, id_num, current_date)