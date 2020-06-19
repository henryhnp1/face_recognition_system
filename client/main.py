from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb as db
from util import ui_loader, db_connector, message_box, standardized, common
from hashlib import md5
import pandas as pd
import csv
import os


ui = ui_loader.load_ui('../resources/main.ui')


class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.frame_main.setHidden(True)
        self.frame_login.setHidden(False)
        self.setWindowTitle("Face Access Control")
        self.handle_buttons()
        self.handle_ui()
        self.handle_combobox()
        self.combobox_setting()
        self.handle_search_line_edit()
        self.session = 'NoOne'
        self.table_widget_setting()
        self.database = db_connector.connector('localhost', 'henrydb', 'root', 'face_recognition')
        if self.database == None:
            msg = message_box.MyMessageBox(QMessageBox.Critical,"Wrong db or authentication", "You must change setting in .config file")
            sys.exit(msg.exec())

        self.handle_ui_login()
        self.button_setting_and_ui()
        self.load_data()
        self.open_window()
        
        #for test ting
        self.handle_frame_ui()

    def check_login(self):
        print(self.session)
        if self.session == None:
            sys.exit()
        if self.session == 'NoOne':
            self.handle_frame_ui()

    def handle_ui(self):
        self.label_username_session.setStyleSheet("QLabel{font-family: ubuntu 30; color: blue; font-weight: bold}")
        self.tabWidget_main.tabBar().setVisible(False)
        self.tabWidget_building_manage.tabBar().setVisible(False)

    def handle_frame_ui(self):
        self.frame_main.setHidden(not self.frame_main.isHidden())
        self.frame_login.setHidden(not self.frame_login.isHidden())

    def handle_ui_login(self):
        self.label_login.setStyleSheet("QLabel{font-family: ubuntu 30; color: blue}")
        self.label_error.setText('')
        self.label_error.setStyleSheet("QLabel{font-family: ubuntu 14; color: red}")
        self.lineEdit_username.setStyleSheet("QLineEdit{border: 1px solid gray; border-radius:10px;}")
        self.lineEdit_password.setStyleSheet("QLineEdit{border: 1px solid gray; border-radius:10px;}")
        self.pushButton_login.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px;"
                                            " background-color: green; color:white}")

    #load_data
    #Todo: load all data when main run
    def load_data(self):
        self.load_building_manage()

    def button_setting_and_ui(self):
        # setting for import file in type of floor table
        self.pushButton_select_file_type_floor.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
        self.pushButton_import_file_type_floor.setEnabled(False)

        # setting for import file in permission table
        self.pushButton_select_file_permission.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
        self.pushButton_import_file_permission.setEnabled(False)
        
    def handle_buttons(self):
        self.pushButton_login.clicked.connect(self.login)
        self.pushButton_logout.clicked.connect(self.logout)
        self.lineEdit_password.returnPressed.connect(self.login)

        # handle button for main manager
        self.pushButton_buiding_manager.clicked.connect(self.open_tab_building)
        self.pushButton_apartment_manager.clicked.connect(self.open_tab_apartment)
        self.pushButton_resident_manager.clicked.connect(self.open_tab_resident)
        self.pushButton_gest_manager.clicked.connect(self.open_tab_guest)
        self.pushButton_video_access_control.clicked.connect(self.open_tab_access_control)

        #handle button for bulding manager
        self.pushButton_block_manage.clicked.connect(self.open_tab_block)
        self.pushButton_floor_manage.clicked.connect(self.open_tab_floor)
        self.pushButton_door_manage.clicked.connect(self.open_tab_door)
        self.pushButton_setting_manage.clicked.connect(self.open_tab_setting)

        ## handle button in setting tab

        ### handle button in type of floor table
        self.pushButton_typeOFloor_add.clicked.connect(self.add_type_of_floor)
        self.pushButton_typeOFloor_edit.clicked.connect(self.edit_type_of_floor)
        self.pushButton_typeOFloor_delete.clicked.connect(self.delete_type_of_floor)
        self.pushButton_select_file_type_floor.clicked.connect(self.select_file_type_of_floor)
        self.pushButton_import_file_type_floor.clicked.connect(self.import_type_of_floor)

        ### handle button in permisson table
        self.pushButton_permission_add.clicked.connect(self.add_permission)
        self.pushButton_permission_edit.clicked.connect(self.edit_permission)
        self.pushButton_permission_delete.clicked.connect(self.delete_permission)
        self.pushButton_select_file_permission.clicked.connect(self.select_file_permission)
        self.pushButton_import_file_permission.clicked.connect(self.import_permission)
    
    def handle_combobox(self):
        # handle action for combobox in buiding manage tab
        ## handle action for combobox in setting tab
        ### handle combobox for type of floor
        self.comboBox_typeOFloor_search.currentTextChanged.connect(self.set_line_search_type_of_building)

        ### handle combobox for permission
        self.comboBox_permission_search.currentTextChanged.connect(self.set_line_search_permission)

    def combobox_setting(self):
        # setting combobox data for satatic combobox
        # setting for building manage tab
        ## setting for setting tab
        ### setting for type of floor table
        type_of_floor_search_fields = ['id', 'name', 'description']
        self.comboBox_typeOFloor_search.addItems(type_of_floor_search_fields)
        
        ### setting for permission table
        permission_search_fields = ['id', 'name', 'description']
        self.comboBox_permission_search.addItems(permission_search_fields)

    def handle_search_line_edit(self):
        # handle line edit using for search
        # handle search line edit for building manage tab
        ## handle search line edit for setting tab
        ### handle seach line edit for type of floor
        self.lineEdit_typeOFloor_search.returnPressed.connect(self.search_type_of_floor)

        ### handle search line edit for permission
        self.lineEdit_search_permission.returnPressed.connect(self.search_permission)

    def login(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        cursor = self.database.cursor()
        cursor.execute("select * from user where username='{}' and password='{}'".format(username, md5(password.encode()).hexdigest()))
        for i in range(cursor.rowcount):
            result = cursor.fetchall()
            if len(result) == 1:
                self.session = username
                cursor.close()
                break
        if self.session:
            self.label_username_session.setText(self.session)
            self.handle_frame_ui()
            self.lineEdit_username.setText('')
            self.lineEdit_password.setText('')
            self.label_error.setText('')
            self.load_data()
        else:
            self.label_error.setText('Wrong username or password')
    
    def logout(self):
        self.session = None
        self.handle_frame_ui()
        # To do: set all line, textedit to ''

    # open tab main

    # default init window
    def open_window(self):
        #for testing
        #self.check_login()
        self.open_tab_building()

    def open_tab_building(self):
        #for testing
        #self.check_login()

        self.tabWidget_main.setCurrentIndex(0)

        common.set_tab_when_clicked(self.pushButton_buiding_manager,
         self.pushButton_buiding_manager, self.pushButton_apartment_manager,
         self.pushButton_resident_manager, self.pushButton_gest_manager,
         self.pushButton_video_access_control)
        
        self.tabWidget_building_manage.setCurrentIndex(0)
        common.set_tab_when_clicked(self.pushButton_block_manage, self.pushButton_floor_manage,
         self.pushButton_door_manage, self.pushButton_setting_manage)

    def open_tab_apartment(self):
        self.tabWidget_main.setCurrentIndex(1)

        common.set_tab_when_clicked(self.pushButton_apartment_manager,
         self.pushButton_buiding_manager, self.pushButton_apartment_manager,
         self.pushButton_resident_manager, self.pushButton_gest_manager,
         self.pushButton_video_access_control)

    def open_tab_resident(self):
        self.tabWidget_main.setCurrentIndex(2)

        common.set_tab_when_clicked(self.pushButton_resident_manager,
         self.pushButton_buiding_manager, self.pushButton_apartment_manager,
         self.pushButton_resident_manager, self.pushButton_gest_manager,
         self.pushButton_video_access_control)

    def open_tab_guest(self):
        self.tabWidget_main.setCurrentIndex(3)

        common.set_tab_when_clicked(self.pushButton_gest_manager,
         self.pushButton_buiding_manager, self.pushButton_apartment_manager,
         self.pushButton_resident_manager, self.pushButton_gest_manager,
         self.pushButton_video_access_control)

    def open_tab_access_control(self):
        self.tabWidget_main.setCurrentIndex(4)

        common.set_tab_when_clicked(self.pushButton_video_access_control,
         self.pushButton_buiding_manager, self.pushButton_apartment_manager,
         self.pushButton_resident_manager, self.pushButton_gest_manager,
         self.pushButton_video_access_control)

    # open tab for building manager
    def open_tab_block(self):
        self.tabWidget_building_manage.setCurrentIndex(0)

        common.set_tab_when_clicked(self.pushButton_block_manage,
         self.pushButton_setting_manage, self.pushButton_door_manage,
         self.pushButton_floor_manage, self.pushButton_block_manage)
    
    def open_tab_floor(self):
        self.tabWidget_building_manage.setCurrentIndex(1)

        common.set_tab_when_clicked(self.pushButton_floor_manage,
         self.pushButton_setting_manage, self.pushButton_door_manage,
         self.pushButton_floor_manage, self.pushButton_block_manage)

    def open_tab_door(self):
        self.tabWidget_building_manage.setCurrentIndex(2)
        common.set_tab_when_clicked(self.pushButton_door_manage,
         self.pushButton_setting_manage, self.pushButton_door_manage,
         self.pushButton_floor_manage, self.pushButton_block_manage)

    def open_tab_setting(self):
        self.tabWidget_building_manage.setCurrentIndex(3)
        common.set_tab_when_clicked(self.pushButton_setting_manage,
         self.pushButton_setting_manage, self.pushButton_door_manage,
         self.pushButton_floor_manage, self.pushButton_block_manage)
        self.load_setting()
    
    # tab setting function
    def load_building_manage(self):
        self.load_setting()
        
    ## load setting data
    def load_setting(self):
        self.load_permission_setting()
        self.load_type_of_floor_setting()
    ## table widget setting
    def table_widget_setting(self):
        ### setting for table widget action type_of_floor
        self.tableWidget_type_of_floor.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget_type_of_floor.itemClicked.connect(self.type_of_floor_click)

        ### setting for table widget action permission
        self.tableWidget_permission.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget_permission.itemClicked.connect(self.permission_click)

    ### function for table type of floor

    ### get data from row in table widget when click to form data in type of floor
    def type_of_floor_click(self):
        current_row = self.tableWidget_type_of_floor.currentRow()
        columns_num = self.tableWidget_type_of_floor.columnCount()
        test = []
        for cell in range(0, columns_num):
            item = self.tableWidget_type_of_floor.item(current_row, cell).text()
            test.append(item)
        self.lineEdit_typeOFloor_id.setText(test[0])
        self.lineEdit_typeOFloor_name.setText(test[1])
        self.textEdit_typeOFloor_description.setText(test[2] if test[2] !='None' else "")

    ### Load data for setting tab
    def load_type_of_floor_setting(self, query=None):
        if query == None:
            query = "select * from type_of_floor"
        cursor = self.database.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            field_names = [x[0] for x in cursor.description]  #get headname
            self.tableWidget_type_of_floor.setRowCount(0)
            self.tableWidget_type_of_floor.setHorizontalHeaderLabels(field_names)  #set headname
            for row_index, row_data in enumerate(data):
                self.tableWidget_type_of_floor.insertRow(row_index)
                for column, item in enumerate(row_data):
                    self.tableWidget_type_of_floor.setItem(row_index, column, QTableWidgetItem(str(item)))
            cursor.close()
        except:
            pass

    ### add type of floor
    def add_type_of_floor(self):
        if self.lineEdit_typeOFloor_name.text().strip():
            name = standardized.str_standard(self.lineEdit_typeOFloor_name.text()).lower()
            description_0 = standardized.str_standard(self.textEdit_typeOFloor_description.toPlainText())
            description = description_0 if description_0 else None
            cursor = self.database.cursor()
            try:
                cursor.execute("insert into type_of_floor(name, description) values(%s, %s)", (name, description))
                self.database.commit()
                self.statusBar().showMessage("New Type Of Floor Added")
                self.load_type_of_floor_setting()
                cursor.close()
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical,"Error data", "name's type of floor exist. Please choose other").exec()
        else:
            message_box.MyMessageBox(QMessageBox.Critical,"Missing data", "Your Name Input Must Be Not Null").exec()

    ### edit type of floor
    def edit_type_of_floor(self):
        if self.lineEdit_typeOFloor_id.text():
            if self.lineEdit_typeOFloor_name.text().strip():
                index = int(self.lineEdit_typeOFloor_id.text())
                name = standardized.str_standard(self.lineEdit_typeOFloor_name.text()).lower()
                description_0 = standardized.str_standard(self.textEdit_typeOFloor_description.toPlainText())
                description = description_0 if description_0 else None
                cursor = self.database.cursor()
                try:
                    cursor.execute("update type_of_floor set name=%s, description=%s where id=%s", (name, description, index))
                    self.database.commit()
                    self.statusBar().showMessage("New Type Of Floor Updated With ID={}".format(index))
                    self.load_type_of_floor_setting()
                    cursor.close()
                except db.Error as e:
                    print(e)
                    message_box.MyMessageBox(QMessageBox.Critical,"Error data", "name's type of floor exist. Please choose other").exec()
            else:
                message_box.MyMessageBox(QMessageBox.Critical,"Missing data", "Your Name Input Must Be Not Null").exec()
    
    ### delete type of floor
    def delete_type_of_floor(self):
        if self.lineEdit_typeOFloor_id.text():
            index = int(self.lineEdit_typeOFloor_id.text())
            cursor = self.database.cursor()
            try:
                cursor.execute("delete from type_of_floor where id=%s", [(index)])
                self.database.commit()
                self.load_type_of_floor_setting()
                self.statusBar().showMessage("A Type Of Floor Deleted With ID={}".format(index))
                cursor.close()
                self.lineEdit_typeOFloor_id.setText(None)
                self.lineEdit_typeOFloor_name.setText(None)
                self.textEdit_typeOFloor_description.setPlainText(None)
            except db.Error as e:
                pass
    
    ### setting line search validator when combobox search changed
    def set_line_search_type_of_building(self):
        field_search = self.comboBox_typeOFloor_search.currentText()
        if field_search == 'id':
            self.lineEdit_typeOFloor_search.setText('')
            self.lineEdit_typeOFloor_search.setValidator(QIntValidator(0, 100000, self))
        else:
            self.lineEdit_typeOFloor_search.setValidator(None)

    ### search function of type of 
    def search_type_of_floor(self):
        field_search = self.comboBox_typeOFloor_search.currentText()
        text_search = self.lineEdit_typeOFloor_search.text()
        if field_search == 'id':
            query = 'select * from type_of_floor where {}={}'.format(field_search, int(text_search))
        else:
            if text_search == None or text_search == '':
                query = 'select * from type_of_floor'
            query = 'select * from type_of_floor where {} like {}'.format(field_search, "'%"+text_search+"%'")
        self.load_type_of_floor_setting(query)
    
    ### select file to import type of floor
    def select_file_type_of_floor(self):
        file_path = QFileDialog.getOpenFileName(self, 'Select File', '/home',"Excel(*.csv *.xlsx)")
        self.pushButton_select_file_type_floor.setText(file_path[0])
        if self.pushButton_select_file_type_floor.text():
            self.pushButton_import_file_type_floor.setEnabled(True)

    ### import type of floor from file
    def import_type_of_floor(self):
        file_path = self.pushButton_select_file_type_floor.text()
        filename, file_extension = os.path.splitext(file_path)
        with open(file_path, mode='rb') as f:
            if file_extension == '.csv':
                reader = pd.read_csv(f)
            else:
                reader = pd.read_excel(f)
            header = reader.columns
            try:
                cursor = self.database.cursor()
                for index, row in reader.iterrows():
                    name = standardized.str_standard(str(row['name']))
                    description = standardized.str_standard(str(row['description']))
                    try:
                        cursor.execute("insert into type_of_floor(name, description) value(%s, %s)", (name, description))
                        self.database.commit()
                    except db.Error as e:
                        pass
                cursor.close()
            except:
                message_box.MyMessageBox(QMessageBox.Critical, "Error", "Incorrect format file!")
        self.load_type_of_floor_setting()


    ### function for permission table

    ### get data from row in table widget when click to form data in permission
    def permission_click(self):
        current_row = self.tableWidget_permission.currentRow()
        columns_num = self.tableWidget_permission.columnCount()
        test = []
        for cell in range(0, columns_num):
            item = self.tableWidget_permission.item(current_row, cell).text()
            test.append(item)
        self.lineEdit_permission_id.setText(test[0])
        self.lineEdit_permission_name.setText(test[1])
        self.textEdit_permission_description.setText(test[2] if test[2] !='None' else "")

    ### add permission to db
    def add_permission(self):
        if self.lineEdit_permission_name.text().strip():
            name = standardized.str_standard(self.lineEdit_permission_name.text()).upper()
            description_0 = standardized.str_standard(self.textEdit_permission_description.toPlainText())
            description = description_0 if description_0 else None
            cursor = self.database.cursor()
            try:
                cursor.execute("insert into permission(name, description) values(%s, %s)", (name, description))
                self.database.commit()
                self.statusBar().showMessage("New Permission Added")
                self.load_permission_setting()
                cursor.close()
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical,"Error data", "name's permssion exist. Please choose other").exec()
        else:
            message_box.MyMessageBox(QMessageBox.Critical,"Missing data", "Your Name Input Must Be Not Null").exec()

    ### edit a permission
    def edit_permission(self):
        if self.lineEdit_permission_id.text():
            if self.lineEdit_permission_name.text().strip():
                index = int(self.lineEdit_permission_id.text())
                name = standardized.str_standard(self.lineEdit_permission_name.text()).upper()
                description_0 = standardized.str_standard(self.textEdit_permission_description.toPlainText())
                description = description_0 if description_0 else None
                cursor = self.database.cursor()
                try:
                    cursor.execute("update permission set name=%s, description=%s where id=%s", (name, description, index))
                    self.database.commit()
                    self.statusBar().showMessage("Permission Updated With ID={}".format(index))
                    self.load_permission_setting()
                    cursor.close()
                except db.Error as e:
                    print(e)
                    message_box.MyMessageBox(QMessageBox.Critical,"Error data", "name's permission exist. Please choose other").exec()
            else:
                message_box.MyMessageBox(QMessageBox.Critical,"Missing data", "Your Name Input Must Be Not Null").exec()

    ### delete a permission
    def delete_permission(self):
        if self.lineEdit_permission_id.text():
            index = int(self.lineEdit_permission_id.text())
            cursor = self.database.cursor()
            try:
                cursor.execute("delete from permission where id=%s", [(index)])
                self.database.commit()
                self.load_permission_setting()
                self.statusBar().showMessage("A Permission Deleted With ID={}".format(index))
                cursor.close()
                self.lineEdit_permission_id.setText(None)
                self.lineEdit_permission_name.setText(None)
                self.textEdit_permission_description.setPlainText(None)
            except db.Error as e:
                pass
    
    ### set line search permission when it's combobox change
    def set_line_search_permission(self):
        field_search = self.comboBox_permission_search.currentText()
        if field_search == 'id':
            self.lineEdit_search_permission.setText('')
            self.lineEdit_search_permission.setValidator(QIntValidator(0, 100000, self))  # 100000 need change in config file 
        else:
            self.lineEdit_search_permission.setValidator(None)

    def select_file_permission(self):
        common.select_file_building_setting(self, self.pushButton_select_file_permission, 
            self.pushButton_import_file_permission)

    def import_permission(self):
        common.import_file_building_setting(self.pushButton_select_file_permission,
         self.database, 'permission', self.load_permission_setting)

    def search_permission(self):
        common.search_common_building_setting(self.comboBox_permission_search,
         self.lineEdit_search_permission, 'permission', self.load_permission_setting)
    
    def load_permission_setting(self, query=None):
        if query == None:
            query = "select * from permission;"
        cursor = self.database.cursor()
        try:
            cursor.execute(query)
            data = cursor.fetchall()
            field_names = [x[0] for x in cursor.description]  #get headname
            self.tableWidget_permission.setRowCount(0)
            self.tableWidget_permission.setHorizontalHeaderLabels(field_names)  #set headname
            for row_index, row_data in enumerate(data):
                self.tableWidget_permission.insertRow(row_index)
                for column, item in enumerate(row_data):
                    self.tableWidget_permission.setItem(row_index, column, QTableWidgetItem(str(item)))
            cursor.close()
        except:
            pass


def main():
    app = QApplication([])
    window = MainApp()
    window.show()
    sys.exit(app.exec())
    window.connector.cursor.close()
    window.connector.close()


if __name__ == '__main__':
    main()
