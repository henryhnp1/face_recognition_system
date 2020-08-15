from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .message_box import MyMessageBox
from .standardized import str_standard
import pandas as pd
import os
import MySQLdb as db
import re
import unicodedata
from datetime import date
from datetime import datetime
from models import my_model
from PyQt5.QtCore import QFileInfo, QSize, Qt
import cv2
import numpy as np
from os import listdir, path
from os.path import isdir
from .detect_face import get_single_bbox_from_image


prototxt = '/home/henry/FinalProject/face_recognition_system/src/data/model/deploy.prototxt'
detect_model = '/home/henry/FinalProject/face_recognition_system/src/data/model/res10_300x300_ssd_iter_140000.caffemodel'

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
    file_path = QFileDialog.getOpenFileName(parent, 'Select File', '/home',"Excel(*.csv)")
    button_select_file.setText(file_path[0])
    if button_select_file.text():
        button_import_file.setEnabled(True)

def select_file_export(parent, button_sellect_file):
    file_path = QFileDialog.getSaveFileName(parent, 'Save File', '/home',"Excel(*.csv)")[0]
    if not QFileInfo(file_path).suffix():
        file_path += '.csv'
    return file_path

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

def export_data_from_table_widget(parrent, table_widget, file_save):
    filename, file_extension = os.path.splitext(file_save)
    with open(file_save, mode='w') as f:
        header = []
        for column in range(table_widget.columnCount()):
            if column == 0:
                next
            else:
                item = table_widget.horizontalHeaderItem(column).text()
                header.append(item)
        df = pd.DataFrame(columns = header)
        index = 0
        for row in range(table_widget.rowCount()):
            rowdata = []
            for column in range(table_widget.columnCount()):
                if column == 0:
                    next
                else:
                    item = table_widget.item(row, column).text()
                    if item is not None:
                        rowdata.append(item)
                    else:
                        rowdata.append('')
            df.loc[index] = rowdata
            index += 1
        if file_extension == '.csv':
            df.to_csv(file_save, index=False)
        else:
            df.to_excel(file_save, index=False)

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
def data_loader_without_change_combobox(parent, database, table, table_data, query=None):
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
    except:
        pass

def delete_item(parent, table, database, index, loader=None, setting_form=None):
    cursor = database.cursor()
    try:
        query = "delete from {} ".format(table)
        cursor.execute(query + "where id=%s", [(index)])
        database.commit()
        if loader: loader()
        parent.statusBar().showMessage("A {} Deleted With ID={}".format(table, index))
        if setting_form: setting_form()
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
        os.mkdir(name_dir)
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
    name = make_acronym_name(no_accent_vietnamese(name)).upper()
    birthdays = birthday.split('-')
    birthday = birthdays[1] + birthdays[2]
    id_num = id_num[-4:]
    now_time = datetime.now()
    hour = now_time.hour
    minute = now_time.minute

    if hour < 10:
        hour = '0' + str(hour)
    else: hour = str(hour)
    if minute < 10:
        minute = '0' + str(minute)
    else: minute = str(minute)

    current_dates = current_date.split('-')
    current_date = hour + '_' + minute + '_' + current_dates[2] + '_' + current_dates[1] + '_' + current_dates[0][-2:]
    return '{}_{}_{}'.format(name+birthday, id_num, current_date)

def get_row_data_item_click(table_data):
    current_row = table_data.currentRow()
    columns_num = table_data.columnCount()
    data = []
    if current_row < 0:
        return None
    for cell in range(0, columns_num):
        item = table_data.item(current_row, cell).text()
        data.append(item)
    return data

def get_single_value_from_table(table, field, where_clause, database):
    query = "select {} from {} {}"
    cursor = database.cursor()
    try:
        cursor.execute(query.format(field, table, where_clause))
        data = cursor.fetchall()
        cursor.close()
        return data[0][0]
    except:
        pass

def get_today_str():
    today = date.today()
    year = str(today.year)
    month = str(today.month)
    day = str(today.day)
    if today.month < 10: month = '0'+month
    if today.day < 10: day = '0'+day
    today_msql = '{}-{}-{}'.format(year, month, day)
    return today_msql

def get_single_item_from_query(query, database):
    cursor = database.cursor()
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data[0]
    except:
        pass

def set_building_combobox_data_change(building_combobox, database):
    building_combobox.clear()
    query_get_building = "select * from building"
    list_building = get_list_model(database, my_model.Building, query_get_building)
    for building in list_building:
        building_model = my_model.Building(*building)
        building_combobox.addItem(building[1], building_model)

def set_floor_combobox_data_change(building_combobox, floor_combobox, type_of_floor, database):
    building_object = building_combobox.currentData()
    if building_object:
        building_id = building_object.pk
        floor_combobox.clear()
        if type_of_floor:
            query_select_floor = '''
                select f.id, f.name as 'floor', b.name as 'building' ,t.name as 'type_of_floor', 
                f.number_of_apartment as 'number_of_apartment' from floor as f
                join building as b on f.building = b.id
                join type_of_floor as t on f.type_of_floor = t.id
                where b.id = {} and t.id = {}
            '''
            data_floor = get_list_model(database, my_model.Floor, query_select_floor.format(building_id, type_of_floor))
        else:
            query_select_floor = '''
                select f.id, f.name as 'floor', b.name as 'building' ,t.name as 'type_of_floor', 
                f.number_of_apartment as 'number_of_apartment' from floor as f
                join building as b on f.building = b.id
                join type_of_floor as t on f.type_of_floor = t.id
                where b.id = {}
            '''
            data_floor = get_list_model(database, my_model.Floor, query_select_floor.format(building_id))

        for floor in data_floor:
            floor_object = my_model.Floor(*floor)
            floor_name = 'Tầng ' + str(floor[1])+' Tòa Nhà ' + floor[2]
            floor_combobox.addItem(floor_name, floor_object)

def set_company_office_combobox_data_change(building_combobox, floor_combobox, company_combobox, database):
    building_object = building_combobox.currentData()
    floor_object = floor_combobox.currentData()
    if building_object and floor_object:
        building_id = building_object.pk
        floor_id = floor_object.pk
        company_combobox.clear()
        query_select_company = '''
            select c.id, c.name, c.phone, c.apartment, a.name as 'office'from company as c
            join apartment as a on c.apartment = a.id
            join floor as f on a.floor = f.id
            join building as b on b.id = f.building
            join type_of_floor as t on t.id = f.type_of_floor
            where t.id = 1 and b.id = {} and f.id = {};
        '''
        data_company = get_list_model(database, my_model.Company, query_select_company.format(building_id, floor_id))
        for company in data_company:
            company_object = my_model.Company(*company)
            comapny_name = 'Công Ty ' + str(company[1]) + ' Phòng ' + company[4]
            company_combobox.addItem(comapny_name, company_object)

def set_apartment_combobox_data_change(building_combobox, floor_combobox, apartment_combobox, database):
    building_object = building_combobox.currentData()
    floor_object = floor_combobox.currentData()
    if building_object and floor_object:
        building_id = building_object.pk
        floor_id = floor_object.pk
        apartment_combobox.clear()
        query_select_apartment = '''
            select a.id, a.name, a.floor, a.status from apartment as a 
            join floor as f on a.floor = f.id
            join building as b on b.id = f.building
            join type_of_floor as t on t.id = f.type_of_floor
            where t.id = 2 and b.id = {} and f.id = {};
        '''
        data_apartment = get_list_model(database, my_model.Apartment, query_select_apartment.format(building_id, floor_id))
        for apartment in data_apartment:
            apartment_object = my_model.Apartment(*apartment)
            apartment_name = 'Phòng ' + apartment_object.name
            apartment_combobox.addItem(apartment_name, apartment_object)

def set_door_combobox_data_change(building_combobox, floor_combobox, door_combobox, database):
    building_object = building_combobox.currentData()
    floor_object = floor_combobox.currentData()
    if building_object and floor_object:
        building_id = building_object.pk
        floor_id = floor_object.pk
        door_combobox.clear()
        query_select_door = '''
            select d.id, d.name, d.floor, d.role from door as d
            join floor as f on d.floor = f.id
            join building as b on b.id = f.building
            join role_door as r on d.role = r.id
            where r.id = 2 and b.id = {} and f.id = {};
        '''
        data_door = get_list_model(database, my_model.Door, query_select_door.format(building_id, floor_id))
        for door in data_door:
            door_object = my_model.Door(*door)
            door_name = 'Cửa ' + str(door_object.name)
            door_combobox.addItem(door_name, door_object)

def set_permisson_door_combobox_data_change(permission_combobox, database):
    permission_combobox.clear()
    query_select_permission = '''
        select * from permission
    '''
    data_permission = get_list_model(database, my_model.Permission, query_select_permission)
    for permission in data_permission:
        permission_object = my_model.Permission(*permission)
        permission_combobox.addItem(permission_object.name, permission_object)

def set_building_combobox_data_change_search(building_combobox, database):
    building_combobox.clear()
    query_get_building = "select * from building"
    list_building = get_list_model(database, my_model.Building, query_get_building)
    building_combobox.addItem('')
    for building in list_building:
        building_model = my_model.Building(*building)
        building_combobox.addItem(building[1], building_model)

def set_floor_combobox_data_change_search(building_combobox, floor_combobox, type_of_floor, database):
    building_object = building_combobox.currentData()
    if building_object:
        building_id = building_object.pk
        floor_combobox.clear()
        if type_of_floor:
            query_select_floor = '''
                select f.id, f.name as 'floor', b.name as 'building' ,t.name as 'type_of_floor', 
                f.number_of_apartment as 'number_of_apartment' from floor as f
                join building as b on f.building = b.id
                join type_of_floor as t on f.type_of_floor = t.id
                where b.id = {} and t.id = {}
            '''
            data_floor = get_list_model(database, my_model.Floor, query_select_floor.format(building_id, type_of_floor))
        else:
            query_select_floor = '''
                select f.id, f.name as 'floor', b.name as 'building' ,t.name as 'type_of_floor', 
                f.number_of_apartment as 'number_of_apartment' from floor as f
                join building as b on f.building = b.id
                join type_of_floor as t on f.type_of_floor = t.id
                where b.id = {}
            '''
            data_floor = get_list_model(database, my_model.Floor, query_select_floor.format(building_id))

        for floor in data_floor:
            floor_object = my_model.Floor(*floor)
            floor_name = 'Tầng ' + str(floor[1])+' Tòa Nhà ' + floor[2]
            floor_combobox.addItem(floor_name, floor_object)
    else:
        floor_combobox.clear()
        floor_combobox.addItem('')


def set_company_office_combobox_data_change_search(building_combobox, floor_combobox, company_combobox, database):
    building_object = building_combobox.currentData()
    floor_object = floor_combobox.currentData()
    if building_object and floor_object:
        building_id = building_object.pk
        floor_id = floor_object.pk
        company_combobox.clear()
        query_select_company = '''
            select c.id, c.name, c.phone, c.apartment, a.name as 'office'from company as c
            join apartment as a on c.apartment = a.id
            join floor as f on a.floor = f.id
            join building as b on b.id = f.building
            join type_of_floor as t on t.id = f.type_of_floor
            where t.id = 1 and b.id = {} and f.id = {};
        '''
        data_company = get_list_model(database, my_model.Company, query_select_company.format(building_id, floor_id))
        for company in data_company:
            company_object = my_model.Company(*company)
            comapny_name = 'Công Ty ' + str(company[1]) + ' Phòng ' + company[4]
            company_combobox.addItem(comapny_name, company_object)
    else:
        company_combobox.clear()
        company_combobox.addItem('')

def set_apartment_combobox_data_change_search(building_combobox, floor_combobox, apartment_combobox, database):
    building_object = building_combobox.currentData()
    floor_object = floor_combobox.currentData()
    if building_object and floor_object:
        building_id = building_object.pk
        floor_id = floor_object.pk
        apartment_combobox.clear()
        query_select_apartment = '''
            select a.id, a.name, a.floor, a.status from apartment as a 
            join floor as f on a.floor = f.id
            join building as b on b.id = f.building
            join type_of_floor as t on t.id = f.type_of_floor
            where t.id = 2 and b.id = {} and f.id = {};
        '''
        data_apartment = get_list_model(database, my_model.Apartment, query_select_apartment.format(building_id, floor_id))
        for apartment in data_apartment:
            apartment_object = my_model.Apartment(*apartment)
            apartment_name = 'Phòng ' + apartment_object.name
            apartment_combobox.addItem(apartment_name, apartment_object)
    else:
        apartment_combobox.clear()
        apartment_combobox.addItem('')

def set_door_combobox_data_change_search(building_combobox, floor_combobox, door_combobox, database):
    building_object = building_combobox.currentData()
    floor_object = floor_combobox.currentData()
    if building_object and floor_object:
        building_id = building_object.pk
        floor_id = floor_object.pk
        door_combobox.clear()
        query_select_door = '''
            select d.id, d.name, d.floor, d.role from door as d
            join floor as f on d.floor = f.id
            join building as b on b.id = f.building
            join role_door as r on d.role = r.id
            where r.id = 2 and b.id = {} and f.id = {};
        '''
        data_door = get_list_model(database, my_model.Door, query_select_door.format(building_id, floor_id))
        for door in data_door:
            door_object = my_model.Door(*door)
            door_name = 'Cửa ' + str(door_object.name)
            door_combobox.addItem(door_name, door_object)
    else:
        door_combobox.clear()
        door_combobox.addItem('')

def setting_clear_ui_select_and_import_file(select_button, import_button):
    import_button.setEnabled(False)
    select_button.setText('Choose File')

def setting_listwidget_image(listwidget, spacing, gridsize, iconsize):
    listwidget.setFlow(QListView.LeftToRight)
    listwidget.setResizeMode(QListView.Adjust)
    listwidget.setSpacing(spacing)
    listwidget.setGridSize(QSize(*gridsize))
    listwidget.setViewMode(QListView.IconMode)
    listwidget.setIconSize(QSize(*iconsize))
    
def add_list_image_to_listwidget(listimage, listWidget):
    for x in listimage:
        image_object = my_model.Image_Person(*x)
        image_name = (image_object.url).split('/')[-1]
        item = QListWidgetItem(image_name)
        item.setData(Qt.UserRole, image_object)
        icon = QIcon()
        pixmap = QPixmap(image_object.url)
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
        item.setIcon(icon)
        listWidget.addItem(item)
fully_query_image_person= '''
    select i.id, i.owner, i.url, i.is_delete from person as p
    join image as i on p.id = i.owner '''

def sort_by_pk(element):
    return element[0]

def load_image_for_image_management(database, person_id, delete_panel, not_delete_panel):
    list_image_delete = get_list_model(database, my_model.Image_Person, fully_query_image_person + 'where i.is_delete = 1 and p.id = {}'.format(int(person_id)))
    list_image_not_delete = get_list_model(database, my_model.Image_Person, fully_query_image_person + 'where i.is_delete = 0 and p.id = {}'.format(int(person_id)))

    sorted(list_image_not_delete, key=sort_by_pk)
    sorted(list_image_delete, key=sort_by_pk)
    delete_panel.clear()
    not_delete_panel.clear()
    setting_listwidget_image(not_delete_panel, spacing=5, gridsize=(210, 210), iconsize=(180, 180))
    add_list_image_to_listwidget(list_image_not_delete, not_delete_panel)

    setting_listwidget_image(delete_panel, spacing=5, gridsize=(210, 210), iconsize=(180, 180))
    add_list_image_to_listwidget(list_image_delete, delete_panel)

def change_item_to_is_delete(database, table, item_id):
    query = 'update {} set is_delete = 1 where id = {}'
    cursor = database.cursor()
    try:
        cursor.execute(query.format(table, int(item_id)))
        database.commit()
    except:
        pass
    cursor.close()

def restore_item(database, table, item_id):
    query = 'update {} set is_delete = 0 where id = {}'
    cursor = database.cursor()
    try:
        cursor.execute(query.format(table, int(item_id)))
        database.commit()
    except:
        pass
    cursor.close()

def crop_face(image, box):
    startX, startY, endX, endY = box
    face = image[startY:endY, startX:endX]
    return face

def save_image(path, person, list_image, name_number, database):
    counter = 1
    query = '''
        insert into image(url, owner, is_delete) values(%s, %s, %s)
    '''
    for image in list_image:
        folder = path + person.name_en + '/'
        image_path = path + '{}/{}.jpg'.format(person.name_en, name_number+counter)
        image_data = (image.data(Qt.UserRole).data)
        make_dir(folder)
        image_data.save(image_path)
        cursor = database.cursor()
        try:
            cursor.execute(query,(image_path, person.pk, 0))
            database.commit()
            counter += 1
        except:
            pass

def import_images_from_folder(parent, images_widget, images_capture, image_folder, flag_anchor, get_face):
    for filename in listdir(image_folder):
        if isdir(filename):
            pass
        else:
            if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                try:
                    filename = image_folder+'/' + filename
                    image = cv2.imread(filename)

                    if add_image_to_list(image, images_capture, QImage.Format_BGR888, get_face):
                        parent.flag_anchor = flag_anchor
                except:
                    next
    
    images_widget.clear()
    for image in images_capture:
        item = QListWidgetItem(str(image.index))
        icon = QIcon()
        icon.addPixmap(image.data, QIcon.Normal, QIcon.Off)
        item.setData(Qt.UserRole, image)
        item.setIcon(icon)
        images_widget.addItem(item)

def select_folder_import_image(parent, button_sellect_folder, button_import_folder):
    folder_path = QFileDialog.getExistingDirectory(parent, 'Select Directory Image')
    button_sellect_folder.setText(folder_path)
    if button_sellect_folder.text():
        button_import_folder.setEnabled(True)

def add_image_to_list(image, images_capture, image_format, get_face):
    if isinstance(image, np.ndarray):
        if images_capture:
            currentImage = images_capture[-1]
            nextIndex = currentImage.index + 1
        else:
            nextIndex = 1
        if get_face:
            box = get_single_bbox_from_image(image, prototxt, detect_model)
            height, width, _ = image.shape
            qt_image = QImage(image.data, width, height, image.strides[0], image_format)
            pixmap = QPixmap.fromImage(qt_image)
            rect = QRect(box[0], box[1], box[2]-box[0], box[3]-box[1])
            pixmap = pixmap.copy(rect)
            pixmap = pixmap.scaled(224, 224)
            image_capture = my_model.ImageCapture(nextIndex, None, pixmap)
            images_capture.append(image_capture)
            return True
        else:
            height, width, _ = image.shape
            qt_image = QImage(image.data, width, height, image.strides[0], image_format)
            pixmap = QPixmap.fromImage(qt_image)
            pixmap = pixmap.scaled(224, 224)
            image_capture = my_model.ImageCapture(nextIndex, None, pixmap)
            images_capture.append(image_capture)
            return True
    else:
        return False