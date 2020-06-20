from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from util import common, standardized, message_box

def building_manage_handle_search_line_edit_setting_tab(self):
    self.lineEdit_typeOFloor_search.returnPressed.connect(self.search_type_of_floor)
    self.lineEdit_search_permission.returnPressed.connect(self.search_permission)

# tab setting function
def building_manage_handle_button_setting_tab(self):
    self.building_manage_handle_button_setting_tab_type_of_floor_table()
    self.building_manage_handle_button_setting_tab_permission_table()

def building_manage_handle_combobox_setting_tab(self):
    ### handle combobox for type of floor
    self.comboBox_typeOFloor_search.currentTextChanged.connect(self.set_line_search_type_of_building)

    ### handle combobox for permission
    self.comboBox_permission_search.currentTextChanged.connect(self.set_line_search_permission)

def building_manage_combobox_setting_data_change_setting_tab(self):
    pass

def building_manage_button_setting_and_ui_setting_tab(self):
    # setting for import file in type of floor table
    self.pushButton_select_file_type_floor.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
    self.pushButton_import_file_type_floor.setEnabled(False)

    # setting for import file in permission table
    self.pushButton_select_file_permission.setStyleSheet("QPushButton{border: 1px solid gray; border-radius:10px; text-align:left}")
    self.pushButton_import_file_permission.setEnabled(False)

### function for table type of floor
def building_manage_setting_tab_table_widget_setting(self):
    self.tableWidget_type_of_floor.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_type_of_floor.itemClicked.connect(self.type_of_floor_click)
    self.tableWidget_type_of_floor.setSortingEnabled(True)

    self.tableWidget_permission.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_permission.itemClicked.connect(self.permission_click)
    self.tableWidget_permission.setSortingEnabled(True)

def building_manage_handle_button_setting_tab_permission_table(self):
    self.pushButton_permission_add.clicked.connect(self.add_permission)
    self.pushButton_permission_edit.clicked.connect(self.edit_permission)
    self.pushButton_permission_delete.clicked.connect(self.delete_permission)
    self.pushButton_select_file_permission.clicked.connect(self.select_file_permission)
    self.pushButton_import_file_permission.clicked.connect(self.import_permission)

def building_manage_handle_button_setting_tab_type_of_floor_table(self):
    self.pushButton_typeOFloor_add.clicked.connect(self.add_type_of_floor)
    self.pushButton_typeOFloor_edit.clicked.connect(self.edit_type_of_floor)
    self.pushButton_typeOFloor_delete.clicked.connect(self.delete_type_of_floor)
    self.pushButton_select_file_type_floor.clicked.connect(self.select_file_type_of_floor)
    self.pushButton_import_file_type_floor.clicked.connect(self.import_type_of_floor)


def building_manage_combobox_setting_setting_tab(self):
    ## setting for setting tab
    ### setting for type of floor table
    self.comboBox_typeOFloor_search.clear()
    type_of_floor_search_fields = ['id', 'name', 'description']
    self.comboBox_typeOFloor_search.addItems(type_of_floor_search_fields)
    
    ### setting for permission table
    self.comboBox_permission_search.clear()
    permission_search_fields = ['id', 'name', 'description']
    self.comboBox_permission_search.addItems(permission_search_fields)

# load setting data
def building_manage_setting_load(self):
    self.load_permission_setting()
    self.load_type_of_floor_setting()

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
#---------------------------------------------------------------------------------------------------------
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