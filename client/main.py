from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb as db
from util import ui_loader, db_connector, message_box, standardized
from hashlib import md5


ui = ui_loader.load_ui('../resources/main.ui')


class MainApp(QMainWindow, ui):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.frame_main.setHidden(True)
        self.frame_login.setHidden(False)
        self.setWindowTitle("Face Access Control")
        self.handle_ui_login()
        self.handle_buttons()
        self.handle_ui()
        self.handle_combobox()
        self.combobox_setting()
        self.handle_search_line_edit()
        self.session = None
        self.table_widget_setting()
        self.database = db_connector.connector('localhost', 'henrydb', 'root', 'face_recognition')
        if self.database == None:
            msg = message_box.MyMessageBox(QMessageBox.Critical,"Wrong db or authentication", "You must change setting in .config file")
            sys.exit(msg.exec())

        #for test ting
        self.handle_frame_ui()
        self.load_data()

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
        self.load_setting()

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
        self.pushButton_typeOFloor_add.clicked.connect(self.add_type_of_floor)
        self.pushButton_typeOFloor_edit.clicked.connect(self.edit_type_of_floor)
        self.pushButton_typeOFloor_delete.clicked.connect(self.delete_type_of_floor)
    
    def handle_combobox(self):
        self.comboBox_typeOFloor_search.currentTextChanged.connect(self.set_line_search_type_of_building)

    def combobox_setting(self):
        type_of_floor_search_fields = ['id', 'name', 'description']
        self.comboBox_typeOFloor_search.addItems(type_of_floor_search_fields)

    def handle_search_line_edit(self):
        self.lineEdit_typeOFloor_search.returnPressed.connect(self.seach_type_of_floor)    

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
    def open_tab_building(self):
        self.tabWidget_main.setCurrentIndex(0)

    def open_tab_apartment(self):
        self.tabWidget_main.setCurrentIndex(1)

    def open_tab_resident(self):
        self.tabWidget_main.setCurrentIndex(2)

    def open_tab_guest(self):
        self.tabWidget_main.setCurrentIndex(3)

    def open_tab_access_control(self):
        self.tabWidget_main.setCurrentIndex(4)

    # open tab for building manager
    def open_tab_block(self):
        self.tabWidget_building_manage.setCurrentIndex(0)
    
    def open_tab_floor(self):
        self.tabWidget_building_manage.setCurrentIndex(1)

    def open_tab_door(self):
        self.tabWidget_building_manage.setCurrentIndex(2)

    def open_tab_setting(self):
        self.tabWidget_building_manage.setCurrentIndex(3)
        self.load_setting()
    
    # tab setting function: setting type_of_floor
    ## table widget setting
    def table_widget_setting(self):
        self.tableWidget_type_of_floor.setSelectionBehavior(QTableView.SelectRows)
        self.tableWidget_type_of_floor.itemClicked.connect(self.type_of_floor_click)

    ## get data from row in table widget when click to form data in type of floor
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

    ## Load data for setting tab
    def load_setting(self, query=None):
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

    ## add type of floor
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
                self.load_setting()
                cursor.close()
            except db.Error as e:
                message_box.MyMessageBox(QMessageBox.Critical,"Error data", "name's type of floor exist. Please choose other").exec()
        else:
            message_box.MyMessageBox(QMessageBox.Critical,"Missing data", "Your Name Input Must Be Not Null").exec()

    ## edit type of floor
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
                    self.load_setting()
                    cursor.close()
                except db.Error as e:
                    print(e)
                    message_box.MyMessageBox(QMessageBox.Critical,"Error data", "name's type of floor exist. Please choose other").exec()
            else:
                message_box.MyMessageBox(QMessageBox.Critical,"Missing data", "Your Name Input Must Be Not Null").exec()
    
    ## delete type of floor
    def delete_type_of_floor(self):
        if self.lineEdit_typeOFloor_id.text():
            index = int(self.lineEdit_typeOFloor_id.text())
            cursor = self.database.cursor()
            try:
                cursor.execute("delete from type_of_floor where id=%s", [(index)])
                self.database.commit()
                self.load_setting()
                self.statusBar().showMessage("A Type Of Floor Deleted With ID={}".format(index))
                cursor.close()
                self.lineEdit_typeOFloor_id.setText(None)
                self.lineEdit_typeOFloor_name.setText(None)
                self.textEdit_typeOFloor_description.setPlainText(None)
            except db.Error as e:
                pass
    
    ## setting line search validator when combobox search changed
    def set_line_search_type_of_building(self):
        field_search = self.comboBox_typeOFloor_search.currentText()
        if field_search == 'id':
            self.lineEdit_typeOFloor_search.setText('')
            self.lineEdit_typeOFloor_search.setValidator(QIntValidator(0, 100000, self))
        else:
            self.lineEdit_typeOFloor_search.setValidator(None)

    ## search function of type of 
    def seach_type_of_floor(self):
        field_search = self.comboBox_typeOFloor_search.currentText()
        text_search = self.lineEdit_typeOFloor_search.text()
        if field_search == 'id':
            query = 'select * from type_of_floor where {}={}'.format(field_search, int(text_search))
        else:
            if text_search == None or text_search == '':
                query = 'select * from type_of_floor'
            query = 'select * from type_of_floor where {} like {}'.format(field_search, "'%"+text_search+"%'")
        self.load_setting(query)

    # tab setting function: setting permission
    ##  

def main():
    app = QApplication([])
    window = MainApp()
    window.show()
    sys.exit(app.exec())
    window.connector.cursor.close()
    window.connector.close()


if __name__ == '__main__':
    main()
