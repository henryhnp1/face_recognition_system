from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox
import pandas as pd
import os
from PyQt5.QtCore import Qt, QRegExp, QDate
import MySQLdb as db

from util import common, standardized, message_box
from models import my_model

fully_query_access_track = '''
    select w.id,b.name as 'building', f.name as 'floor', d.name as 'door', w.name as 'name_en', 
    p.name, p.id_card , pm.name as 'permission', w.time_in, w.image from warning as w
    join door as d on w.door = d.id
    join floor as f on d.floor = f.id
    join building as b on f.building = b.id
    join permission as pm on w.permission = pm.id
    left join person as p on w.name = p.name_en
'''
def admin_acesss_control_access_track_clear_form(self):
    self.comboBox_fields_search_access_track.setCurrentIndex(0)
    self.lineEdit_search_access_control_access_track.setText(None)
    self.frame_access_track_warning_image.setStyleSheet("border: 0px")

def access_control_access_track_load(self):
    self.admin_acesss_control_access_track_clear_form()
    common.data_loader(self,self.database, '', self.tableWidget_admin_access_track, fully_query_access_track)

def access_control_handle_button_access_track_tab(self):
    self.pushButton_export_admin_access_track.clicked.connect(self.access_control_access_track_export)

def access_control_handle_combobox_access_track_tab(self):
    self.comboBox_fields_search_access_track.currentTextChanged.connect(self.access_control_access_track_setting_line_search)

def access_control_combobox_setting_access_track_tab(self):
    field_search = ['id', 'building', 'floor', 'door', 'name', 'name en', 'id card']
    self.comboBox_fields_search_access_track.addItems(field_search)

def access_control_combobox_setting_data_change_access_track_tab(self):
    pass

def access_control_handle_search_line_edit_access_track_tab(self):
    self.lineEdit_search_access_control_access_track.returnPressed.connect(self.access_control_access_track_search)

def access_control_table_widget_setting_access_track_tab(self):
    self.tableWidget_admin_access_track.setSortingEnabled(True)
    self.tableWidget_admin_access_track.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_admin_access_track.itemClicked.connect(self.access_control_access_track_item_click)

def access_control_button_setting_and_ui_access_track_tab(self):
    pass

def access_control_access_track_export(self):
    if self.tableWidget_admin_access_track.rowCount():
        path_file = common.select_file_export(self, self.pushButton_export_admin_access_track)
        if path_file:
            common.export_data_from_table_widget(self, self.tableWidget_admin_access_track, path_file)
            self.statusBar().showMessage("Export Success")
    else:
        message_box.MyMessageBox(QMessageBox.Critical, 'Error', 'No data to export')

def access_control_access_track_setting_line_search(self):
    field_search = self.comboBox_fields_search_access_track.currentText()
    if field_search == 'id' or field_search=='id_card' or field_search == 'floor':
        self.lineEdit_search_access_control_access_track.setText('')
        self.lineEdit_search_access_control_access_track.setValidator(QRegExpValidator(QRegExp("[0-9]{0,12}")))
    else:
        self.lineEdit_search_access_control_access_track.setValidator(None)

def access_control_access_track_search(self):
    field_search = self.comboBox_fields_search_access_track.currentText()
    text_search = self.lineEdit_search_access_control_access_track.text()
    query = '''
        select w.id,b.name as 'building', f.name as 'floor', d.name as 'door', w.name as 'name_en', 
        p.name, p.id_card , pm.name as 'permission', w.time_in, w.image from warning as w
        join door as d on w.door = d.id
        join floor as f on d.floor = f.id
        join building as b on f.building = b.id
        join permission as pm on w.permission = pm.id
        left join person as p on w.name = p.name_en {}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("where w.id like '%{}%'".format(int(text_search)))
    elif field_search == 'name':
        query = query.format("where p.name like '%{}%'".format(text_search))
    elif field_search == 'id card':
        query = query.format("where p.id_card like '%{}%'".format(text_search))
    elif field_search == 'name en':
        query = query.format("where w.name like '%{}%'".format(text_search))
    elif field_search == 'door':
        query = query.format("where d.name like '%{}%'".format(text_search))
    elif field_search == 'floor':
        query = query.format("where f.name like '%{}%'".format(text_search))
    elif field_search == 'building':
        query = query.format("where b.name like '%{}%'".format(text_search))
    else:
        query = query.format('')
    common.data_loader_without_change_combobox(self, self.database, 'None', self.tableWidget_admin_access_track, query) 

def access_control_access_track_item_click(self):
    data = common.get_row_data_item_click(self.tableWidget_admin_access_track)
    if data:
        wat_object = my_model.WarningAccessTrack(*data)
        self.frame_access_track_warning_image.setStyleSheet("border: 0px; background-image: url('{}'); background-repeat: no-repeat;".format(wat_object.image))