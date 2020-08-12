from PyQt5.QtWidgets import QTableView
from PyQt5.QtGui import QIntValidator

from util import common, standardized, message_box

# tab block manage function
def building_manage_block_manage_tab_table_widget_setting(self):
    self.tableWidget_block.setSelectionBehavior(QTableView.SelectRows)
    self.tableWidget_block.itemClicked.connect(self.building_manage_block_manage_block_item_click)
    self.tableWidget_block.setSortingEnabled(True)

def building_manage_combobox_setting_block_manage_tab(self):
    ## setting for block manage tab
    self.comboBox_search_block.clear()
    block_search_fields = ['id', 'name', 'location']
    self.comboBox_search_block.addItems(block_search_fields)

def building_manage_combobox_setting_data_change_block_manage_tab(self):
    pass

def building_manage_handle_combobox_block_manage_tab(self):
    ## handle action for combobox in block manage tab
    self.comboBox_search_block.currentTextChanged.connect(self.building_manage_block_manage_setting_line_search)

def building_manage_handle_button_block_manage_tab(self):
    self.pushButton_add_block.clicked.connect(self.building_manage_block_manage_add_block)
    self.pushButton_edit_block.clicked.connect(self.building_manage_block_manage_edit_block)
    self.pushButton_delete_block.clicked.connect(self.building_manage_block_manage_delete_block)

def building_manage_button_setting_and_ui_block_tab(self):
    pass

def building_manage_handle_search_line_edit_block_tab(self):
    self.lineEdit_search_block.returnPressed.connect(self.building_manage_block_manage_search_block)

def building_manage_block_manage_load(self, query=None):
    common.data_loader(self, self.database, "building", self.tableWidget_block, query)

def building_manage_block_manage_add_block(self):
    if self.lineEdit_name_block.text().strip():
        name = standardized.str_standard(self.lineEdit_name_block.text()).upper()
        location_0 = standardized.str_standard(self.lineEdit_location_block.text())
        location = location_0 if location_0 else None
        num_of_floor = self.spinBox_numOfFloor_block.value()
        arceage = self.doubleSpinBox_acreage_block.value()
        cursor = self.database.cursor()
        try:
            cursor.execute("insert into building(name, location, number_of_floor, acreage) values(%s, %s, %s, %s)",
                (name, location, num_of_floor, arceage))
            self.database.commit()
            self.statusBar().showMessage("New Building Added")
            self.building_manage_block_manage_load()
            cursor.close()
        except db.Error as e:
            message_box.MyMessageBox(QMessageBox.Critical,"Error data", "name's type of floor exist. Please choose other").exec()
    else:
        message_box.MyMessageBox(QMessageBox.Critical,"Missing data", "Your Name Input Must Be Not Null").exec()

def building_manage_block_manage_edit_block(self):
    if self.lineEdit_id_block.text():
        if self.lineEdit_name_block.text().strip():
            index = int(self.lineEdit_id_block.text())
            name = standardized.str_standard(self.lineEdit_name_block.text()).upper()
            location_0 = standardized.str_standard(self.lineEdit_location_block.text())
            location = location_0 if location_0 else None
            num_of_floor = self.spinBox_numOfFloor_block.value()
            acreage = self.doubleSpinBox_acreage_block.value()
            cursor = self.database.cursor()
            try:
                cursor.execute("update building set name=%s, location=%s, number_of_floor=%s, acreage=%s where id=%s",
                    (name, location, num_of_floor, acreage, index))
                self.database.commit()
                self.statusBar().showMessage("Building Updated With ID={}".format(index))
                self.building_manage_block_manage_load()
                cursor.close()
            except db.Error as e:
                print(e)
                message_box.MyMessageBox(QMessageBox.Critical,"Error data", "name's permission exist. Please choose other").exec()
        else:
            message_box.MyMessageBox(QMessageBox.Critical,"Missing data", "Your Name Input Must Be Not Null").exec()

def building_manage_block_manage_delete_block(self):
    if self.lineEdit_id_block.text():
        index = int(self.lineEdit_id_block.text())   
        common.delete_item(self, 'building', self.database, index,
            self.building_manage_block_manage_load, self.building_manage_block_manage_setting_blank_form)

def building_manage_block_manage_search_block(self):
    field_search = self.comboBox_search_block.currentText()
    text_search = self.lineEdit_search_block.text()
    if field_search == 'id':
        query = 'select * from building where {}={}'.format(field_search, int(text_search))
    else:
        if text_search == None or text_search == '':
            query = 'select * from building'
        query = 'select * from building where {} like {}'.format(field_search, "'%"+text_search+"%'")
    self.building_manage_block_manage_load(query)

def building_manage_block_manage_setting_line_search(self):
    field_search = self.comboBox_search_block.currentText()
    if field_search == 'id':
        self.lineEdit_search_block.setText('')
        self.lineEdit_search_block.setValidator(QIntValidator(0, 100000, self))
    else:
        self.lineEdit_search_block.setValidator(None)

def building_manage_block_manage_block_item_click(self):
    current_row = self.tableWidget_block.currentRow()
    columns_num = self.tableWidget_block.columnCount()
    test = []
    for cell in range(0, columns_num):
        item = self.tableWidget_block.item(current_row, cell).text()
        test.append(item)
    self.lineEdit_id_block.setText(test[0])
    self.lineEdit_name_block.setText(test[1])
    self.spinBox_numOfFloor_block.setValue(int(test[3]))
    self.lineEdit_location_block.setText(test[2] if test[2] !='None' else "")
    self.lineEdit_location_block.setCursorPosition(0)
    self.doubleSpinBox_acreage_block.setValue(float(test[4]))

def building_manage_block_manage_setting_blank_form(self):
    self.lineEdit_id_block.setText(None)
    self.lineEdit_name_block.setText(None)
    self.spinBox_numOfFloor_block.setValue(0)
    self.lineEdit_location_block.setText(None)
    self.doubleSpinBox_acreage_block.setValue(0)

