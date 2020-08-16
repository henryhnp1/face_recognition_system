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
select_lastest_image_for_guest = '''
    select i.id, i.owner, i.url, i.is_delete from image as i join person as p
    on i.owner = p.id
    where p.is_resident = 0 and i.owner = {} order by i.id desc limit 1;
'''

fully_query_guest = '''
    select p.id, p.name, p.birthday, p.id_card, p.phone, p.name_en from person as p where p.is_resident = 0
'''

fully_query_image_guest_delete= '''
    select i.id, i.owner, i.url, i.is_delete from person as p
    join image as i on p.id = i.owner
    where i.is_delete = 1 and p.is_resident = 0
'''
fully_query_image_guest_not_delete= '''
    select i.id, i.owner, i.url, i.is_delete from person as p
    join image as i on p.id = i.owner
    where i.is_delete = 0 and p.is_resident = 0
'''
def security_guest_image_clear_form(self):
    self.listWidget_image_capturing_guest.clear()
    self.listWidget_image_guest_not_delete.clear()
    self.listWidget_image_guest_delete.clear()
    self.images_capture_guest.clear()
    self.pushButton_select_guest_image.setText('Choose folder')
    self.pushButton_import_guest_image.setEnabled(False)

def security_guest_image_load(self):
    self.security_guest_image_clear_form_and_ui()
    self.security_guest_image_load_guest_table()

def security_guest_image_handle_button_guest_image_tab(self):
    self.pushButton_guest_image_manage_photo.clicked.connect(self.security_guest_image_open_tab_manage_photo)
    self.pushButton_guest_image_add_photo.clicked.connect(self.security_guest_image_open_tab_add_photo)
    self.pushButton_guest_start_capture.clicked.connect(self.capture_image.startVideoCapture)
    self.pushButton_guest_stop_capture.clicked.connect(self.security_guest_image_stop_camera_capture)
    self.pushButton_select_guest_image.clicked.connect(self.security_guest_image_select_folder_image)
    self.pushButton_import_guest_image.clicked.connect(self.security_guest_image_import_folder_image)
    # self.pushButton_capture_image_admin.clicked.connect(self.video.capturing)

def security_guest_image_handle_combobox_guest_image_tab(self):
    self.comboBox_fields_search_guest_image.currentTextChanged.connect(self.security_guest_image_setting_line_search)

def security_guest_image_combobox_setting_guest_image_tab(self):
    field_searchs = ['id', 'name', 'id_card', 'phone', 'name encode']
    self.comboBox_fields_search_guest_image.addItems(field_searchs)

    field_option_face = ['Find Face', 'No Action']
    self.comboBox_option_get_face_guest.addItems(field_option_face)

def security_guest_image_combobox_setting_data_change_guest_image_tab(self):
    pass

def security_guest_image_handle_search_line_edit_guest_image_tab(self):
    self.lineEdit_type_search_guest_image.returnPressed.connect(self.security_guest_image_search)

def security_guest_image_table_widget_setting_guest_image_tab(self):
    self.security_guest_image_item_image_click()
    self.tableWidget_guest_image_info.setSortingEnabled(True)
    self.tableWidget_guest_image_info.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_guest_image_info.itemClicked.connect(self.security_guest_image_item_click)
    
def security_guest_image_button_setting_and_ui_guest_image_tab(self):
    self.tabWidget_guest_image_management.tabBar().setVisible(False)
    self.pushButton_guest_start_capture.setEnabled(True)
    self.pushButton_guest_stop_capture.setEnabled(False)
    self.pushButton_guest_capturing.setEnabled(False)
    self.listWidget_image_capturing_guest.setSelectionMode(QAbstractItemView.ExtendedSelection)
    common.setting_listwidget_image(self.listWidget_image_capturing_guest, 5, (200, 200), (180, 180))
    self.pushButton_select_guest_image.setStyleSheet('QPushButton{text-align:right}')
    self.pushButton_import_guest_image.setEnabled(False)

def security_guest_image_load_guest_table(self):
    common.data_loader(self, self.database, 'None', self.tableWidget_guest_image_info, fully_query_guest)

def security_guest_image_item_click(self):
    self.listWidget_image_guest_not_delete.clear()
    self.listWidget_image_guest_delete.clear()

    data = common.get_row_data_item_click(self.tableWidget_guest_image_info)
    common.load_image_for_image_management(self.database, data[0], self.listWidget_image_guest_delete, self.listWidget_image_guest_not_delete, True)

def security_guest_image_open_tab_manage_photo(self):
    self.tabWidget_guest_image_management.setCurrentIndex(0)
    common.set_tab_when_clicked(self.pushButton_guest_image_manage_photo, self.pushButton_guest_image_add_photo)
    data = common.get_row_data_item_click(self.tableWidget_guest_image_info)
    if data:
        self.security_guest_image_item_click()

def security_guest_image_open_tab_add_photo(self):
    self.tabWidget_guest_image_management.setCurrentIndex(1)
    common.set_tab_when_clicked(self.pushButton_guest_image_add_photo, self.pushButton_guest_image_manage_photo)
   
def security_guest_image_setting_line_search(self):
    field_search = self.comboBox_fields_search_guest_image.currentText()
    if field_search == 'id' or field_search=='id_card' or field_search=='phone':
        self.lineEdit_type_search_guest_image.setText('')
        self.lineEdit_type_search_guest_image.setValidator(QRegExpValidator(QRegExp("[0-9]{0,12}")))
    else:
        self.lineEdit_type_search_guest_image.setValidator(None)

def security_guest_image_item_image_click(self):
    self.listWidget_image_guest_not_delete.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.listWidget_image_guest_delete.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.listWidget_image_guest_not_delete.setContextMenuPolicy(Qt.CustomContextMenu)
    self.listWidget_image_guest_delete.setContextMenuPolicy(Qt.CustomContextMenu)
    self.listWidget_image_guest_not_delete.customContextMenuRequested[QPoint].connect(self.security_guest_image_image_not_delete_click)
    self.listWidget_image_guest_delete.customContextMenuRequested[QPoint].connect(self.security_guest_image_image_delete_click)
    self.listWidget_image_capturing_guest.setContextMenuPolicy(Qt.CustomContextMenu)
    self.listWidget_image_capturing_guest.customContextMenuRequested[QPoint].connect(self.security_guest_image_image_capture_click)

def security_guest_image_image_not_delete_click(self):
    image_item = self.listWidget_image_guest_not_delete.currentItem().data(Qt.UserRole)
    rightMenu = QMenu(self.listWidget_image_guest_not_delete)
    removeAction = QAction(u"Delete", self, triggered = self.security_guest_image_change_image_to_delete)
    rightMenu.addAction(removeAction)
    rightMenu.exec_(QCursor.pos())

def security_guest_image_image_capture_click(self):
    image_item = self.listWidget_image_capturing_guest.currentItem().data(Qt.UserRole)
    rightMenu = QMenu(self.listWidget_image_capturing_guest)
    removeAction = QAction(u"Delete", self, triggered = self.security_guest_image_delete_image_capture)
    addAction = QAction(u"Add", self, triggered = self.security_guest_image_add_image_capture)
    rightMenu.addAction(removeAction)
    rightMenu.addAction(addAction)
    rightMenu.exec_(QCursor.pos())

def security_guest_image_restore_image(self):
    images_selected = self.listWidget_image_guest_delete.selectedItems()
    for image_item in images_selected:
        image_item_data = image_item.data(Qt.UserRole)
        common.restore_item(self.database, 'image', image_item_data.pk)
    common.load_image_for_image_management(self.database, image_item_data.owner, self.listWidget_image_guest_delete, self.listWidget_image_guest_not_delete)

def security_guest_image_image_delete_click(self):
    image_item = self.listWidget_image_guest_delete.currentItem().data(Qt.UserRole)
    rightMenu = QMenu(self.listWidget_image_guest_delete)
    removeAction = QAction(u"Delete", self, triggered = self.security_guest_image_delete_image)
    restoreAction = QAction(u"Restore", self, triggered = self.security_guest_image_restore_image)
    rightMenu.addAction(removeAction)
    rightMenu.addAction(restoreAction)
    rightMenu.exec_(QCursor.pos())

def security_guest_image_delete_image(self):
    images_selected = self.listWidget_image_guest_delete.selectedItems()
    for image_item in images_selected:
        image_item_data = image_item.data(Qt.UserRole)
        common.delete_item(self, 'image', self.database, image_item_data.pk)
    common.load_image_for_image_management(self.database, image_item_data.owner, self.listWidget_image_guest_delete, self.listWidget_image_guest_not_delete)
    
def security_guest_image_change_image_to_delete(self):
    images_selected = self.listWidget_image_guest_not_delete.selectedItems()
    for image_item in images_selected:
        image_item_data = image_item.data(Qt.UserRole)
        common.change_item_to_is_delete(self.database, 'image', image_item_data.pk)
    common.load_image_for_image_management(self.database, image_item_data.owner, self.listWidget_image_guest_delete, self.listWidget_image_guest_not_delete)

def security_guest_image_delete_image_capture(self):
    images_selected = self.listWidget_image_capturing_guest.selectedItems()
    for image_item in images_selected:
        image_data = image_item.data(Qt.UserRole)
        self.images_capture_guest.remove(image_data)
        self.listWidget_image_capturing_guest.takeItem(self.listWidget_image_capturing_guest.row(image_item))
    if len(self.images_capture) == 0:
        self.flag_anchor = None

def security_guest_image_add_image_capture(self):
    data = common.get_row_data_item_click(self.tableWidget_guest_image_info)
    if data:
        guest = my_model.PersonDraffInfo(*data)
        warning = QMessageBox.question(self, 'Choose guest add image', "Would you want to add images selected for {}?".format(guest.name_en), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if warning == QMessageBox.Yes:
            images_selected = self.listWidget_image_capturing_guest.selectedItems()
            folder_path = '/home/henry/FinalProject/face_recognition_system/src/data/dataset/processed/'
            last_image_for_guest = common.get_single_item_from_query(select_lastest_image_for_guest.format(guest.pk),self.database)
            if last_image_for_guest:
                last_image_name = (my_model.Image_Person(*last_image_for_guest)).url.split('/')[-1]
                name_number = last_image_name.split('.')[0]
            else:
                name_number = 0

            common.save_image(folder_path, guest, images_selected, int(name_number), self.database)
            for image in images_selected:
                self.listWidget_image_capturing_guest.takeItem(self.listWidget_image_capturing_guest.row(image))
                self.images_capture_guest.remove(image.data(Qt.UserRole))
                if len(self.images_capture) == 0:
                    self.flag_anchor = None
    else:
        message_box.MyMessageBox(QMessageBox.Critical, 'Error', 'No Person Selected. Please select a guest in the top table').exec()

@pyqtSlot()
def on_pushButton_guest_start_capture_clicked(self):
    self.pushButton_guest_start_capture.setEnabled(False)
    self.security_guest_image_setting_button_capture()
    self.thread.start()
    if not self.capture_image.video_capture.isOpened():
        self.capture_image.video_capture = cv2.VideoCapture(0)
    self.capture_image.moveToThread(self.thread)
    self.image_viewer = video_stream.ImageViewer()
    layout = QVBoxLayout()
    self.frame_video_capture_guest.setLayout(layout)
    layout.addWidget(self.image_viewer)

    self.capture_image.video_signal.connect(self.image_viewer.setImage)

def security_guest_image_stop_camera_capture(self):
    self.pushButton_guest_start_capture.setEnabled(True)
    self.security_guest_image_setting_button_capture()
    self.stop_capture = True
    cv2.destroyAllWindows()
    self.capture_image.video_capture.release()
    
@pyqtSlot()
def on_pushButton_guest_capturing_clicked(self):
    # guest_data = self.tableWidget_guest_image_info
    image = self.image_viewer.image_cv.copy()
    if common.add_image_to_list(image, self.images_capture_guest, QImage.Format_RGB888, True):
        self.flag_anchor = '041'

    self.listWidget_image_capturing_guest.clear()
    for image in self.images_capture_guest:
        item = QListWidgetItem(str(image.index))
        icon = QIcon()
        icon.addPixmap(image.data, QIcon.Normal, QIcon.Off)
        item.setData(Qt.UserRole, image)
        item.setIcon(icon)
        self.listWidget_image_capturing_guest.addItem(item)

def security_guest_image_setting_button_capture(self):
    if self.pushButton_guest_start_capture.isEnabled():
        self.pushButton_guest_stop_capture.setEnabled(False)
        self.pushButton_guest_capturing.setEnabled(False)
    if not self.pushButton_guest_start_capture.isEnabled():
        self.pushButton_guest_stop_capture.setEnabled(True)
        self.pushButton_guest_capturing.setEnabled(True)

def security_guest_image_clear_form_and_ui(self):
    self.pushButton_guest_start_capture.setEnabled(True)
    self.listWidget_image_guest_not_delete.clear()
    self.listWidget_image_guest_delete.clear()
    self.listWidget_image_capturing_guest.clear()

def security_guest_image_select_folder_image(self):
    common.select_folder_import_image(self, self.pushButton_select_guest_image, self.pushButton_import_guest_image)

def security_guest_image_import_folder_image(self):
    image_folder = self.pushButton_select_guest_image.text()
    text_get_face = self.comboBox_option_get_face_guest.currentText()
    find_face = None
    if text_get_face == 'Find Face':
        find_face = True
    common.import_images_from_folder(self, self.listWidget_image_capturing_guest, self.images_capture_guest, image_folder, '211', find_face)
    self.pushButton_select_guest_image.setText('Choose folder')
    self.pushButton_import_guest_image.setEnabled(False)

def security_guest_image_search(self):
    field_search = self.comboBox_fields_search_guest_image.currentText()
    text_search = self.lineEdit_type_search_guest_image.text()

    query = '''
        select p.id, p.name, p.birthday, p.id_card, p.phone, p.name_en from person as p where p.is_resident = 0 {}
    '''
    if text_search == '':
        query = query.format('')
    elif field_search == 'id':
        query = query.format("and p.id like '%{}%'".format(int(text_search)))
    elif field_search == 'name':
        query = query.format("and p.name like '%{}%'".format(text_search))
    elif field_search == 'id card':
        query = query.format("and p.id_card like '%{}%'".format(text_search))
    elif field_search == 'phone':
        query = query.format("and p.phone like '%{}%'".format(text_search))
    elif field_search == 'name encode':
        query = query.format("and p.name_en like '%{}%'".format(text_search))
    common.data_loader(self, self.database, 'None', self.tableWidget_guest_image_info, query)