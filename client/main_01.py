# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_01.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1262, 877)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(220, 140, 851, 531))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_login = QtWidgets.QLabel(self.frame)
        self.label_login.setGeometry(QtCore.QRect(270, 70, 311, 71))
        font = QtGui.QFont()
        font.setPointSize(40)
        font.setBold(True)
        font.setWeight(75)
        self.label_login.setFont(font)
        self.label_login.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login.setObjectName("label_login")
        self.label_error = QtWidgets.QLabel(self.frame)
        self.label_error.setGeometry(QtCore.QRect(200, 160, 451, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_error.setFont(font)
        self.label_error.setAlignment(QtCore.Qt.AlignCenter)
        self.label_error.setObjectName("label_error")
        self.label_username = QtWidgets.QLabel(self.frame)
        self.label_username.setGeometry(QtCore.QRect(170, 230, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_username.setFont(font)
        self.label_username.setObjectName("label_username")
        self.label_password = QtWidgets.QLabel(self.frame)
        self.label_password.setGeometry(QtCore.QRect(170, 310, 101, 17))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_password.setFont(font)
        self.label_password.setObjectName("label_password")
        self.pushButton_login = QtWidgets.QPushButton(self.frame)
        self.pushButton_login.setGeometry(QtCore.QRect(360, 390, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_login.setFont(font)
        self.pushButton_login.setObjectName("pushButton_login")

        self.lineEdit_username = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_username.setGeometry(QtCore.QRect(310, 220, 291, 31))
        self.lineEdit_username.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.lineEdit_username.setFocus()
        
        self.lineEdit_password = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_password.setGeometry(QtCore.QRect(310, 290, 291, 31))
        self.lineEdit_password.setObjectName("lineEdit_password")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1262, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_login.setText(_translate("MainWindow", "LOGIN"))
        self.label_error.setText(_translate("MainWindow", "Error"))
        self.label_username.setText(_translate("MainWindow", "Username"))
        self.label_password.setText(_translate("MainWindow", "Password"))
        self.pushButton_login.setText(_translate("MainWindow", "Login"))
        self.lineEdit_username.setPlaceholderText(_translate("MainWindow", "Enter your username"))
        self.lineEdit_password.setPlaceholderText(_translate("MainWindow", "Enter your password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

