# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signup.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Signup(object):
    def setupUi(self, Signup):
        Signup.setObjectName("Signup")
        Signup.resize(595, 456)
        self.centralwidget = QtWidgets.QWidget(Signup)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 40, 60, 30))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(200, 120, 215, 118))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.line_pwd = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_pwd.setObjectName("line_pwd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.line_pwd)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.line_balance = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_balance.setObjectName("line_balance")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.line_balance)
        self.line_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.line_name.setObjectName("line_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.line_name)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(200, 300, 215, 50))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_register = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_register.setObjectName("btn_register")
        self.horizontalLayout.addWidget(self.btn_register)
        self.btn_quit = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_quit.setObjectName("btn_quit")
        self.horizontalLayout.addWidget(self.btn_quit)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(160, 80, 301, 17))
        self.label_5.setObjectName("label_5")
        Signup.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Signup)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 595, 28))
        self.menubar.setObjectName("menubar")
        Signup.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Signup)
        self.statusbar.setObjectName("statusbar")
        Signup.setStatusBar(self.statusbar)

        self.retranslateUi(Signup)
        self.btn_quit.clicked.connect(Signup.close)
        QtCore.QMetaObject.connectSlotsByName(Signup)

    def retranslateUi(self, Signup):
        _translate = QtCore.QCoreApplication.translate
        Signup.setWindowTitle(_translate("Signup", "MainWindow"))
        self.label.setText(_translate("Signup", "Register"))
        self.label_2.setText(_translate("Signup", "Name:"))
        self.label_3.setText(_translate("Signup", "Password:"))
        self.label_4.setText(_translate("Signup", "Asset"))
        self.btn_register.setText(_translate("Signup", "Register"))
        self.btn_quit.setText(_translate("Signup", "Exit"))
        self.label_5.setText(_translate("Signup", "Register:"))

