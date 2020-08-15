from PyQt5.QtGui import QIntValidator, QRegExpValidator, QPixmap, QIcon, QCursor, QImage
from PyQt5.QtWidgets import QTableView, QCompleter, QComboBox, QMessageBox, QLabel, QGridLayout, QMenu, QAction, QAbstractItemView
from PyQt5.QtWidgets import QScrollArea, QGroupBox, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QListView, QHBoxLayout
from PyQt5.QtCore import QSize, Qt, QRegExp, QDate, QPoint, QThread, QObject, QCoreApplication,pyqtSlot, QRect
import pandas as pd
import os
import MySQLdb as db
import cv2
import numpy as np

from util import common, standardized, message_box, video_stream, detect_face
from models import my_model

prototxt = '/home/henry/FinalProject/face_recognition_system/src/data/model/deploy.prototxt'
detect_model = '/home/henry/FinalProject/face_recognition_system/src/data/model/res10_300x300_ssd_iter_140000.caffemodel'
select_lastest_image_for_person = '''
    select i.id, i.owner, i.url, i.is_delete from image as i join person as p
    on i.owner = p.id
    where i.owner = {} order by i.id desc limit 1;
'''
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
def admin_access_control_person_image_clear_form(self):
    self.listWidget_image_capturing.clear()
    self.listWidget_image_ndelete_admin_panel.clear()
    self.listWidget_image_delete_admin_panel.clear()
    self.images_capture.clear()
    self.pushButton_select_person_image.setText('Choose folder')
    self.pushButton_import_person_image.setEnabled(False)

def access_control_person_image_load(self):
    self.access_control_person_image_clear_form_and_ui()
    self.access_control_person_image_load_person_table()

def access_control_handle_button_person_image_tab(self):
    self.pushButton_person_manage_manage_photo.clicked.connect(self.access_control_person_image_open_tab_manage_photo)
    self.pushButton_person_manage_add_photo.clicked.connect(self.access_control_person_image_open_tab_add_photo)
    self.pushButton_start_cam_admin.clicked.connect(self.capture_image.startVideoCapture)
    self.pushButton_stop_cam_admin.clicked.connect(self.access_control_person_image_stop_camera_capture)
    self.pushButton_select_person_image.clicked.connect(self.access_control_person_image_select_folder_image)
    self.pushButton_import_person_image.clicked.connect(self.access_control_person_image_import_folder_image)
    # self.pushButton_capture_image_admin.clicked.connect(self.video.capturing)

def access_control_handle_combobox_person_image_tab(self):
    self.comboBox_fields_search_person_image.currentTextChanged.connect(self.access_control_person_image_setting_line_search)

def access_control_combobox_setting_person_image_tab(self):
    field_searchs = ['id', 'name', 'id_card', 'phone', 'name encode']
    self.comboBox_fields_search_person_image.addItems(field_searchs)

    field_option_face = ['Find Face', 'No Action']
    self.comboBox_option_get_face.addItems(field_option_face)

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
    self.frame_person_image_admin.setStyleSheet("QFrame{border: 0px}")
    self.tabWidget_person_image_manage.tabBar().setVisible(False)
    self.pushButton_start_cam_admin.setEnabled(False)
    self.pushButton_stop_cam_admin.setEnabled(False)
    self.pushButton_capture_image_admin.setEnabled(False)
    self.listWidget_image_capturing.setSelectionMode(QAbstractItemView.ExtendedSelection)
    common.setting_listwidget_image(self.listWidget_image_capturing, 5, (200, 200), (180, 180))
    self.pushButton_select_person_image.setStyleSheet('QPushButton{text-align:right}')
    

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

def access_control_person_image_open_tab_manage_photo(self):
    self.tabWidget_person_image_manage.setCurrentIndex(0)
    common.set_tab_when_clicked(self.pushButton_person_manage_manage_photo, self.pushButton_person_manage_add_photo)
    data = common.get_row_data_item_click(self.tableWidget_person_image_info)
    if data:
        self.access_control_person_image_item_click()

def access_control_person_image_open_tab_add_photo(self):
    self.tabWidget_person_image_manage.setCurrentIndex(1)
    common.set_tab_when_clicked(self.pushButton_person_manage_add_photo, self.pushButton_person_manage_manage_photo)
   
def access_control_person_image_setting_line_search(self):
    field_search = self.comboBox_fields_search_person_image.currentText()
    if field_search == 'id' or field_search=='id_card' or field_search=='phone':
        self.lineEdit_type_search_person_image.setText('')
        self.lineEdit_type_search_person_image.setValidator(QRegExpValidator(QRegExp("[0-9]{0,12}")))
    else:
        self.lineEdit_type_search_person_image.setValidator(None)

def access_control_person_image_item_image_click(self):
    self.listWidget_image_ndelete_admin_panel.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.listWidget_image_delete_admin_panel.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.listWidget_image_ndelete_admin_panel.setContextMenuPolicy(Qt.CustomContextMenu)
    self.listWidget_image_delete_admin_panel.setContextMenuPolicy(Qt.CustomContextMenu)
    self.listWidget_image_ndelete_admin_panel.customContextMenuRequested[QPoint].connect(self.access_control_person_image_image_not_delete_click)
    self.listWidget_image_delete_admin_panel.customContextMenuRequested[QPoint].connect(self.access_control_person_image_image_delete_click)
    self.listWidget_image_capturing.setContextMenuPolicy(Qt.CustomContextMenu)
    self.listWidget_image_capturing.customContextMenuRequested[QPoint].connect(self.access_control_person_image_image_capture_click)

def access_control_person_image_image_not_delete_click(self):
    image_item = self.listWidget_image_ndelete_admin_panel.currentItem().data(Qt.UserRole)
    rightMenu = QMenu(self.listWidget_image_ndelete_admin_panel)
    removeAction = QAction(u"Delete", self, triggered = self.access_control_person_image_change_image_to_delete)
    rightMenu.addAction(removeAction)
    rightMenu.exec_(QCursor.pos())

def access_control_person_image_image_capture_click(self):
    image_item = self.listWidget_image_capturing.currentItem().data(Qt.UserRole)
    rightMenu = QMenu(self.listWidget_image_capturing)
    removeAction = QAction(u"Delete", self, triggered = self.access_control_person_image_delete_image_capture)
    addAction = QAction(u"Add", self, triggered = self.access_control_person_image_add_image_capture)
    rightMenu.addAction(removeAction)
    rightMenu.addAction(addAction)
    rightMenu.exec_(QCursor.pos())

def access_control_person_image_restore_image(self):
    images_selected = self.listWidget_image_delete_admin_panel.selectedItems()
    for image_item in images_selected:
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
    images_selected = self.listWidget_image_delete_admin_panel.selectedItems()
    for image_item in images_selected:
        image_item_data = image_item.data(Qt.UserRole)
        common.delete_item(self, 'image', self.database, image_item_data.pk)
    common.load_image_for_image_management(self.database, image_item_data.owner, self.listWidget_image_delete_admin_panel, self.listWidget_image_ndelete_admin_panel)
    
def access_control_person_image_change_image_to_delete(self):
    images_selected = self.listWidget_image_ndelete_admin_panel.selectedItems()
    for image_item in images_selected:
        image_item_data = image_item.data(Qt.UserRole)
        common.change_item_to_is_delete(self.database, 'image', image_item_data.pk)
    common.load_image_for_image_management(self.database, image_item_data.owner, self.listWidget_image_delete_admin_panel, self.listWidget_image_ndelete_admin_panel)

def access_control_person_image_delete_image_capture(self):
    images_selected = self.listWidget_image_capturing.selectedItems()
    for image_item in images_selected:
        image_data = image_item.data(Qt.UserRole)
        self.images_capture.remove(image_data)
        self.listWidget_image_capturing.takeItem(self.listWidget_image_capturing.row(image_item))
    if len(self.images_capture) == 0:
        self.flag_anchor = None

def access_control_person_image_add_image_capture(self):
    data = common.get_row_data_item_click(self.tableWidget_person_image_info)
    if data:
        person = my_model.PersonDraffInfo(*data)
        warning = QMessageBox.question(self, 'Choose person add image', "Would you want to add images selected for {}?".format(person.name_en), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            images_selected = self.listWidget_image_capturing.selectedItems()
            folder_path = '/home/henry/FinalProject/face_recognition_system/src/data/dataset/processed/'
            last_image_for_person = common.get_single_item_from_query(select_lastest_image_for_person.format(person.pk),self.database)
            if last_image_for_person:
                last_image_name = (my_model.Image_Person(*last_image_for_person)).url.split('/')[-1]
                name_number = last_image_name.split('.')[0]
            else:
                name_number = 0

            common.save_image(folder_path, person, images_selected, int(name_number), self.database)
            for image in images_selected:
                self.listWidget_image_capturing.takeItem(self.listWidget_image_capturing.row(image))
                self.images_capture.remove(image.data(Qt.UserRole))
                if len(self.images_capture) == 0:
                    self.flag_anchor = None
    else:
        message_box.MyMessageBox(QMessageBox.Critical, 'Error', 'No Person Selected. Please select a person in the top table').exec()

@pyqtSlot()
def on_pushButton_start_cam_admin_clicked(self):
    self.pushButton_start_cam_admin.setEnabled(False)
    self.access_control_person_image_setting_button_capture()
    self.thread.start()
    if not self.capture_image.video_capture.isOpened():
        self.capture_image.video_capture = cv2.VideoCapture(0)
    self.capture_image.moveToThread(self.thread)
    self.image_viewer = video_stream.ImageViewer()
    layout = QVBoxLayout()
    self.frame_video_capture_admin.setLayout(layout)
    layout.addWidget(self.image_viewer)

    self.capture_image.video_signal.connect(self.image_viewer.setImage)

def access_control_person_image_stop_camera_capture(self):
    self.pushButton_start_cam_admin.setEnabled(True)
    self.access_control_person_image_setting_button_capture()
    self.stop_capture = True
    cv2.destroyAllWindows()
    self.capture_image.video_capture.release()
    
@pyqtSlot()
def on_pushButton_capture_image_admin_clicked(self):
    # person_data = self.tableWidget_person_image_info
    image = self.image_viewer.image_cv.copy()
    if common.add_image_to_list(image, self.images_capture, QImage.Format_RGB888, True):
        self.flag_anchor = '041'

    self.listWidget_image_capturing.clear()
    for image in self.images_capture:
        item = QListWidgetItem(str(image.index))
        icon = QIcon()
        icon.addPixmap(image.data, QIcon.Normal, QIcon.Off)
        item.setData(Qt.UserRole, image)
        item.setIcon(icon)
        self.listWidget_image_capturing.addItem(item)

def access_control_person_image_setting_button_capture(self):
    if self.pushButton_start_cam_admin.isEnabled():
        self.pushButton_stop_cam_admin.setEnabled(False)
        self.pushButton_capture_image_admin.setEnabled(False)
    if not self.pushButton_start_cam_admin.isEnabled():
        self.pushButton_stop_cam_admin.setEnabled(True)
        self.pushButton_capture_image_admin.setEnabled(True)

def access_control_person_image_clear_form_and_ui(self):
    self.pushButton_start_cam_admin.setEnabled(True)
    self.listWidget_image_ndelete_admin_panel.clear()
    self.listWidget_image_delete_admin_panel.clear()
    self.listWidget_image_capturing.clear()

def access_control_person_image_select_folder_image(self):
    common.select_folder_import_image(self, self.pushButton_select_person_image, self.pushButton_import_person_image)

def access_control_person_image_import_folder_image(self):
    image_folder = self.pushButton_select_person_image.text()
    text_get_face = self.comboBox_option_get_face.currentText()
    find_face = None
    if text_get_face == 'Find Face':
        find_face = True
    common.import_images_from_folder(self, self.listWidget_image_capturing, self.images_capture, image_folder, '041', find_face)
    self.pushButton_select_person_image.setText('Choose folder')
    self.pushButton_import_person_image.setEnabled(False)