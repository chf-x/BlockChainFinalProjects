# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bank.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Bank(object):
    def setupUi(self, Bank):
        Bank.setObjectName("Bank")
        Bank.resize(736, 497)
        self.centralwidget = QtWidgets.QWidget(Bank)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_quit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quit.setGeometry(QtCore.QRect(500, 330, 90, 25))
        self.btn_quit.setObjectName("btn_quit")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(90, 330, 320, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(100)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_authorize = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_authorize.setObjectName("btn_authorize")
        self.horizontalLayout.addWidget(self.btn_authorize)
        self.btn_reject = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_reject.setObjectName("btn_reject")
        self.horizontalLayout.addWidget(self.btn_reject)
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(190, 130, 350, 150))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 70, 221, 17))
        self.label.setObjectName("label")
        Bank.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Bank)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 736, 28))
        self.menubar.setObjectName("menubar")
        Bank.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Bank)
        self.statusbar.setObjectName("statusbar")
        Bank.setStatusBar(self.statusbar)

        self.retranslateUi(Bank)
        QtCore.QMetaObject.connectSlotsByName(Bank)

    def retranslateUi(self, Bank):
        _translate = QtCore.QCoreApplication.translate
        Bank.setWindowTitle(_translate("Bank", "MainWindow"))
        self.btn_quit.setText(_translate("Bank", "Exit"))
        self.btn_authorize.setText(_translate("Bank", "Identify"))
        self.btn_reject.setText(_translate("Bank", "Concel"))
        self.label.setText(_translate("Bank", "select:"))

