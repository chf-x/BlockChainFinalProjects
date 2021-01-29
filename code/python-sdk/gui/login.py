# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(687, 450)
        self.centralwidget = QtWidgets.QWidget(Login)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(140, 90, 391, 30))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(220, 150, 215, 81))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.line_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_name.setObjectName("line_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.line_name)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.line_pwd = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_pwd.setObjectName("line_pwd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.line_pwd)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(190, 330, 282, 50))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_login = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_login.setObjectName("btn_login")
        self.horizontalLayout.addWidget(self.btn_login)
        self.btn_quit = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_quit.setObjectName("btn_quit")
        self.horizontalLayout.addWidget(self.btn_quit)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(296, 40, 81, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(160, 120, 391, 17))
        self.label_5.setObjectName("label_5")
        self.btn_signup = QtWidgets.QPushButton(self.centralwidget)
        self.btn_signup.setGeometry(QtCore.QRect(340, 270, 80, 25))
        self.btn_signup.setObjectName("btn_signup")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(210, 270, 141, 17))
        self.label_6.setObjectName("label_6")
        Login.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Login)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 687, 28))
        self.menubar.setObjectName("menubar")
        Login.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Login)
        self.statusbar.setObjectName("statusbar")
        Login.setStatusBar(self.statusbar)

        self.retranslateUi(Login)
        self.btn_quit.clicked.connect(Login.close)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "MainWindow"))
        self.label.setText(_translate("Login", "Welcome!"))
        self.label_3.setText(_translate("Login", "Password"))
        self.label_2.setText(_translate("Login", "Company name"))
        self.btn_login.setText(_translate("Login", "Confirm"))
        self.btn_quit.setText(_translate("Login", "Exit"))
        self.label_4.setText(_translate("Login", "Welcome！"))
        self.label_5.setText(_translate("Login", "Register"))
        self.btn_signup.setText(_translate("Login", "Register"))
        self.label_6.setText(_translate("Login", "Register:"))

