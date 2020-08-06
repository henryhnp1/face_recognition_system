from PyQt5.QtGui import QIntValidator, QRegExpValidator, QPixmap, QIcon, QCursor
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox, QLabel, QGridLayout, QMenu, QAction
from PyQt5.QtWidgets import QScrollArea, QGroupBox, QPushButton, QHBoxLayout, QListWidget, QListWidgetItem, QListView
from PyQt5.QtCore import QSize, Qt, QRegExp, QDate, QPoint
import pandas as pd
import os
import MySQLdb as db

from util import common, standardized, message_box, video_stream
from models import my_model

fully_query_person = '''
    select p.id, p.name, p.birthday, p.id_card, p.phone, p.name_en from person as p
'''
fully_query_image_person_delete= '''
    select i.id, i.owner, i.url, i.is_delete from person as p
    join image as i on p.id = i.owner
    where i.is_delete = 1 
'''
fully_query_image_person_not_delete= '''
    select i.id, i.owner, i.url, i.is_delete from person as p
    join image as i on p.id = i.owner
    where i.is_delete = 0 
'''

def access_control_person_image_load(self):
    self.access_control_person_image_load_person_table()

def access_control_handle_button_person_image_tab(self):
    self.pushButton_person_manage_manage_photo.clicked.connect(self.access_control_person_image_open_tab_manage_photo)
    self.pushButton_person_manage_add_photo.clicked.connect(self.access_control_person_image_open_tab_add_photo)

def access_control_handle_combobox_person_image_tab(self):
    self.comboBox_fields_search_person_image.currentTextChanged.connect(self.access_control_person_image_setting_line_search)

def access_control_combobox_setting_person_image_tab(self):
    field_searchs = ['id', 'name', 'id_card', 'phone', 'name encode']
    self.comboBox_fields_search_person_image.addItems(field_searchs)

def access_control_combobox_setting_data_change_person_image_tab(self):
    pass

def access_control_handle_search_line_edit_person_image_tab(self):
    pass

def access_control_table_widget_setting_person_image_tab(self):
    self.access_control_person_image_item_image_click()
    self.tableWidget_person_image_info.setSortingEnabled(True)
    self.tableWidget_person_image_info.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_person_image_info.itemClicked.connect(self.access_control_person_image_item_click)
    

def access_control_button_setting_and_ui_person_image_tab(self):
    self.tabWidget_person_image_manage.tabBar().setVisible(False)

def access_control_person_image_load_person_table(self):
    common.data_loader(self, self.database, 'None', self.tableWidget_person_image_info, fully_query_person)

def access_control_person_image_load_image_delete(self):
    pass
    # list_image_delete = common.get_list_model(self.database, my_model.Image_Person, fully_query_image_person_delete)

def access_control_person_image_load_image_not_delete(self):
    pass
    # list_image_not_delete = common.get_list_model(self.database, my_model.Image_Person, fully_query_image_person_not_delete) 

def access_control_person_image_item_click(self):
    self.listWidget_image_ndelete_admin_panel.clear()
    self.listWidget_image_delete_admin_panel.clear()

    data = common.get_row_data_item_click(self.tableWidget_person_image_info)

    common.load_image_for_image_management(self.database, data[0], self.listWidget_image_delete_admin_panel, self.listWidget_image_ndelete_admin_panel)

    # list_image_delete = common.get_list_model(self.database, my_model.Image_Person, fully_query_image_person_delete + 'and p.id = {}'.format(int(data[0])))
    # list_image_not_delete = common.get_list_model(self.database, my_model.Image_Person, fully_query_image_person_not_delete + 'and p.id = {}'.format(int(data[0])))

    # common.setting_listwidget_image(self.listWidget_image_ndelete_admin_panel, spacing=5, gridsize=(196, 196), iconsize=(190, 190))
    # common.add_list_image_to_listwidget(list_image_not_delete, self.listWidget_image_ndelete_admin_panel)

    # common.setting_listwidget_image(self.listWidget_image_delete_admin_panel, spacing=5, gridsize=(196, 196), iconsize=(190, 190))
    # common.add_list_image_to_listwidget(list_image_delete, self.listWidget_image_delete_admin_panel)
    

def access_control_person_image_open_tab_manage_photo(self):
    self.tabWidget_person_image_manage.setCurrentIndex(0)
    common.set_tab_when_clicked(self.pushButton_person_manage_manage_photo, self.pushButton_person_manage_add_photo)

def access_control_person_image_open_tab_add_photo(self):
    self.tabWidget_person_image_manage.setCurrentIndex(1)
    common.set_tab_when_clicked(self.pushButton_person_manage_add_photo, self.pushButton_person_manage_manage_photo)

    # label = QLabel(self.groupBox_video_capture_image)
    # label.resize(280, 280)
    # th = video_stream.Thread(self.groupBox_video_capture_image)
    # th.changePixmap.connect(self.groupBox_video_capture_image.label.setPixmap(QPixmap.fromImage()))
    # th.start()

def access_control_person_image_setting_line_search(self):
    field_search = self.comboBox_fields_search_person_image.currentText()
    if field_search == 'id' or field_search=='id_card' or field_search=='phone':
        self.lineEdit_type_search_person_image.setText('')
        self.lineEdit_type_search_person_image.setValidator(QRegExpValidator(QRegExp("[0-9]{0,12}")))
    else:
        self.lineEdit_type_search_person_image.setValidator(None)

def access_control_person_image_item_image_click(self):
    self.listWidget_image_ndelete_admin_panel.setContextMenuPolicy(Qt.CustomContextMenu)
    self.listWidget_image_delete_admin_panel.setContextMenuPolicy(Qt.CustomContextMenu)
    self.listWidget_image_ndelete_admin_panel.customContextMenuRequested[QPoint].connect(self.access_control_person_image_image_not_delete_click)
    self.listWidget_image_delete_admin_panel.customContextMenuRequested[QPoint].connect(self.access_control_person_image_image_delete_click)

def access_control_person_image_image_not_delete_click(self):
    image_item = self.listWidget_image_ndelete_admin_panel.currentItem().data(Qt.UserRole)
    rightMenu = QMenu(self.listWidget_image_ndelete_admin_panel)
    removeAction = QAction(u"Delete", self, triggered = self.access_control_person_image_change_image_to_delete)
    rightMenu.addAction(removeAction)
    rightMenu.exec_(QCursor.pos())
    
def access_control_person_image_restore_image(self):
    image_item = self.listWidget_image_delete_admin_panel.currentItem()
    image_item_data = image_item.data(Qt.UserRole)
    common.restore_item(self.database, 'image', image_item_data.pk)
    common.load_image_for_image_management(self.database, image_item_data.owner, self.listWidget_image_delete_admin_panel, self.listWidget_image_ndelete_admin_panel)

def access_control_person_image_image_delete_click(self):
    image_item = self.listWidget_image_delete_admin_panel.currentItem().data(Qt.UserRole)
    rightMenu = QMenu(self.listWidget_image_ndelete_admin_panel)
    removeAction = QAction(u"Delete", self, triggered = self.access_control_person_image_delete_image)
    restoreAction = QAction(u"Restore", self, triggered = self.access_control_person_image_restore_image)
    rightMenu.addAction(removeAction)
    rightMenu.addAction(restoreAction)
    rightMenu.exec_(QCursor.pos())

def access_control_person_image_delete_image(self):
    image_item = self.listWidget_image_delete_admin_panel.currentItem()
    image_item_data = image_item.data(Qt.UserRole)
    common.delete_item(self, 'image', self.database, image_item_data.pk)
    common.load_image_for_image_management(self.database, image_item_data.owner, self.listWidget_image_delete_admin_panel, self.listWidget_image_ndelete_admin_panel)
    

def access_control_person_image_change_image_to_delete(self):
    image_item = self.listWidget_image_ndelete_admin_panel.currentItem()
    image_item_data = image_item.data(Qt.UserRole)
    common.change_item_to_is_delete(self.database, 'image', image_item_data.pk)
    common.load_image_for_image_management(self.database, image_item_data.owner, self.listWidget_image_delete_admin_panel, self.listWidget_image_ndelete_admin_panel)
