from PyQt5.QtGui import QIntValidator, QRegExpValidator, QPixmap, QIcon, QCursor, QImage
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox, QLabel, QGridLayout, QMenu, QAction, QAbstractItemView
from PyQt5.QtWidgets import QScrollArea, QGroupBox, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QListView, QHBoxLayout
from PyQt5.QtCore import QSize, Qt, QRegExp, QDate, QPoint, QThread, QObject, QCoreApplication,pyqtSlot, QRect
import pandas as pd
import os
import MySQLdb as db
import cv2
import numpy as np

from tensorflow.keras.models import load_model

from util import common, standardized, message_box, video_stream, detect_face
from models import my_model

fully_query_select_track = '''
    select h.id, p.name, p.name_en, p.id_card, p.phone, p.village, b.name as 'building', 
    f.name as 'floor', d.name as 'door', pm.name as 'role', h.time, h.url from history_out_int as h
    join person as p on p.id = h.person
    join door as d on h.door = d.id
    join floor as f on f.id = d.floor
    join building as b on f.building = b.id
    join permission as pm on pm.id = h.permission {}
'''

def security_acesss_control_access_track_clear_form(self):
    self.lineEdit_search_access_track_security.setText(None)
    self.lineEdit_access_track_person_id.setText(None)
    self.lineEdit_access_track_person_name.setText(None)
    self.lineEdit_access_track_person_id_num.setText(None)
    self.textEdit_access_track_person_info.setPlainText(None)
    self.lineEdit_access_track_block.setText(None)
    self.lineEdit_access_track_floor.setText(None)
    self.lineEdit_access_track_door.setText(None)
    self.comboBox_access_track_role_security_permission.setCurrentIndex(0)
    self.comboBox_access_track_camera_setting_buidling.setCurrentIndex(0)

def security_access_control_access_track_load(self):
    self.security_acesss_control_access_track_clear_form()
    common.data_loader(self, self.database, '', self.tableWidget_access_track_security, fully_query_select_track.format(''))

def security_access_control_access_track_load_table(self):
    common.data_loader(self, self.database, '', self.tableWidget_access_track_security, fully_query_select_track.format(''))

def security_access_control_handle_button_access_track_tab(self):
    self.pushButton_start_camera_track.clicked.connect(self.video_track.startVideoTrack)
    self.pushButton_stop_camera_track.clicked.connect(self.security_access_control_access_track_stop_camera_capture)
    self.pushButton_export_track.clicked.connect(self.security_access_control_access_track_export)
    self.pushButton_access_track_update_accident_securety.clicked.connect(self.security_access_control_access_track_update)
    self.pushButton_load_data_access_track_security.clicked.connect(self.security_access_control_access_track_load_table)

def security_access_control_handle_combobox_access_track_tab(self):
    self.comboBox_fields_search_access_track_security.currentTextChanged.connect(self.security_access_control_access_track_setting_line_search)
    self.comboBox_access_track_camera_setting_buidling.currentTextChanged.connect(self.security_access_control_combobox_setting_data_change_access_track_tab_floor_combobox)
    self.comboBox_access_track_camera_setting_floor.currentTextChanged.connect(self.security_access_control_combobox_setting_data_change_access_track_tab_door_combobox)
    self.comboBox_access_track_camera_setting_door.currentTextChanged.connect(self.security_access_control_setting_door)

def security_access_control_combobox_setting_access_track_tab(self):
    field_search = ['id', 'id card', 'phone', 'name', 'name en', 'building', 'floor', 'door','permission']
    self.comboBox_fields_search_access_track_security.addItems(field_search)

def security_access_control_handle_search_line_edit_access_track_tab(self):
    self.lineEdit_search_access_track_security.returnPressed.connect(self.security_access_control_access_track_search)

def security_access_control_table_widget_setting_access_track_tab(self):
    self.tableWidget_access_track_security.setSortingEnabled(True)
    self.tableWidget_access_track_security.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_access_track_security.itemClicked.connect(self.security_access_control_access_track_item_click)

def security_access_control_button_setting_and_ui_access_track_tab(self):
    self.pushButton_start_camera_track.setEnabled(True)
    self.pushButton_stop_camera_track.setEnabled(False)

def security_setting_button_capture(self):
    if self.pushButton_start_camera_track.isEnabled():
        self.pushButton_stop_camera_track.setEnabled(False)
    else:
        self.pushButton_stop_camera_track.setEnabled(True)

def security_access_control_combobox_setting_data_change_access_track_tab(self):
    self.security_access_control_combobox_setting_data_change_access_track_tab_building_combobox()

def security_access_control_combobox_setting_data_change_access_track_tab_building_combobox(self):
    common.set_building_combobox_data_change(self.comboBox_access_track_camera_setting_buidling, self.database)

def security_access_control_combobox_setting_data_change_access_track_tab_floor_combobox(self):
    common.set_floor_combobox_data_change(self.comboBox_access_track_camera_setting_buidling, self.comboBox_access_track_camera_setting_floor, None, self.database)

def security_access_control_combobox_setting_data_change_access_track_tab_door_combobox(self):
    common.set_door_combobox_data_change(self.comboBox_access_track_camera_setting_buidling, self.comboBox_access_track_camera_setting_floor, self.comboBox_access_track_camera_setting_door, self.database)

def security_access_control_access_track_setting_line_search(self):
    field_search = self.comboBox_fields_search_access_track_security.currentText()
    if field_search == 'id' or field_search=='id_card' or field_search=='phone' or field_search=='door' or field_search=='foor' :
        self.lineEdit_search_access_track_security.setText('')
        self.lineEdit_search_access_track_security.setValidator(QRegExpValidator(QRegExp("[0-9]{0,12}")))
    else:
        self.lineEdit_search_access_track_security.setValidator(None)

def security_access_control_access_track_item_click(self):
    data = common.get_row_data_item_click(self.tableWidget_access_track_security)
    if data:
        history_io = my_model.CustomeHistoryOutIn(*data)
        self.lineEdit_access_track_person_id.setText(history_io.pk)
        self.lineEdit_access_track_person_name.setText(history_io.name)
        self.lineEdit_access_track_person_id_num.setText(history_io.id_card)
        
        self.lineEdit_access_track_block.setText(history_io.building)
        self.lineEdit_access_track_floor.setText(history_io.floor)
        self.lineEdit_access_track_door.setText(history_io.door)
        text_info = 'Name_en: ' + history_io.name_en + '\nPhone: ' + history_io.phone + '\nVillage: ' + history_io.village
        self.textEdit_access_track_person_info.setPlainText(text_info)

        self.dateTimeEdit_access_track_time_accident_securety.setDateTime(common.get_datetime_from_datetime_data(history_io.time_in))
        index_role = self.comboBox_access_track_role_security_permission.findText(history_io.role)
        self.comboBox_access_track_role_security_permission.setCurrentIndex(index_role)


def security_access_control_access_track_update(self):
    id_history_io = self.lineEdit_access_track_person_id.text()
    if id_history_io:
        role = self.comboBox_access_track_role_security_permission.currentIndex() + 1
        common.update_table(self.database, 'history_out_int',  "permission = {} where id = {} ".format(role, int(id_history_io)))
        self.security_access_control_access_track_load_table()
    else:
        message_box.MyMessageBox(QMessageBox.Critical, 'Error', 'No data to update')

def security_access_control_access_track_export(self):
    if self.tableWidget_access_track_security.rowCount():
        path_file = common.select_file_export(self, self.pushButton_export_track)
        if path_file:
            common.export_data_from_table_widget(self, self.tableWidget_access_track_security, path_file)
            self.statusBar().showMessage("Export Success")
    else:
        message_box.MyMessageBox(QMessageBox.Critical, 'Error', 'No data to export')

def security_access_control_access_track_search(self):
    field_search = self.comboBox_fields_search_access_track_security.currentText()
    text_search = self.lineEdit_search_access_track_security.text()
    query = '''
        select h.id, p.name, p.name_en, p.id_card, p.phone, p.village, b.name as 'building', 
        f.name as 'floor', d.name as 'door', pm.name as 'role', h.time, h.url from history_out_int as h
        join person as p on p.id = h.person
        join door as d on h.door = d.id
        join floor as f on f.id = d.floor
        join building as b on f.building = b.id
        join permission as pm on pm.id = h.permission {}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("where h.id like '%{}%'".format(int(text_search)))
    elif field_search == 'name':
        query = query.format("where p.name like '%{}%'".format(text_search))
    elif field_search == 'id card':
        query = query.format("where p.id_card like '%{}%'".format(text_search))
    elif field_search == 'phone':
        query = query.format("where p.phone like '%{}%'".format(text_search))
    elif field_search == 'name en':
        query = query.format("where p.name_en like '%{}%'".format(text_search))
    elif field_search == 'door':
        query = query.format("where d.name like '%{}%'".format(text_search))
    elif field_search == 'building':
        query = query.format("where b.name like '%{}%'".format(text_search))
    elif field_search == 'floor':
        query = query.format("where f.name like '%{}%'".format(text_search))
    elif field_search == 'permission':
        query = query.format("where pm.name like '%{}%'".format(text_search))
    else:
        query = query.format("and p.village like '%{}%'".format(text_search))

    common.data_loader_without_change_combobox(self, self.database, 'None', self.tableWidget_access_track_security, query)

@pyqtSlot()
def on_pushButton_start_camera_track_clicked(self):

    if self.metadata['predict_model_path'] and self.metadata['embedded_face_path']:
        self.metadata['confidence'] = 0.8
        self.metadata['database'] = self.database
        self.metadata['announce'] = self.label_result_track
        self.metadata['recognition'] = 1
        self.video_track.set_metadata(self.metadata)

        self.pushButton_start_camera_track.setEnabled(False)
        self.security_setting_button_capture()
        self.thread.start()
        if not self.video_track.video_capture.isOpened():
            self.video_track.video_capture = cv2.VideoCapture(0)
        self.video_track.moveToThread(self.thread)
        self.image_viewer_track = video_stream.ImageViewer()
        layout = QVBoxLayout()
        self.frame_security_video_track.setLayout(layout)
        layout.addWidget(self.image_viewer_track)
        self.video_track.video_signal.connect(self.image_viewer_track.setImage)
    else:
        message_box.MyMessageBox(QMessageBox.Critical, 'Error', 'No data Classify')

def security_access_control_access_track_stop_camera_capture(self):
    self.pushButton_start_camera_track.setEnabled(True)
    self.security_setting_button_capture()
    self.stop_capture = True
    cv2.destroyAllWindows()
    self.video_track.video_capture.release()
    self.flag_classify = False

def security_access_control_setting_door(self):
    door_object = self.comboBox_access_track_camera_setting_door.currentData()
    if door_object:
        self.metadata['door'] = door_object.pk
        print(self.metadata['door'])
        