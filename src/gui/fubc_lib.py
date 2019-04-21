# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fubc_lib.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StackedWidget(object):
    def setupUi(self, StackedWidget):
        StackedWidget.setObjectName("StackedWidget")
        StackedWidget.resize(837, 455)
        StackedWidget.setStyleSheet("Fusion")
        self.LoginPage = QtWidgets.QWidget()
        self.LoginPage.setObjectName("LoginPage")
        self.formLayout_3 = QtWidgets.QFormLayout(self.LoginPage)
        self.formLayout_3.setContentsMargins(11, 300, -1, 11)
        self.formLayout_3.setObjectName("formLayout_3")
        self.formLayoutLabels = QtWidgets.QFormLayout()
        self.formLayoutLabels.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.formLayoutLabels.setHorizontalSpacing(4)
        self.formLayoutLabels.setVerticalSpacing(2)
        self.formLayoutLabels.setObjectName("formLayoutLabels")
        self.user_label = QtWidgets.QLabel(self.LoginPage)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.user_label.setFont(font)
        self.user_label.setObjectName("user_label")
        self.formLayoutLabels.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.user_label)
        self.pass_label = QtWidgets.QLabel(self.LoginPage)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pass_label.setFont(font)
        self.pass_label.setIndent(12)
        self.pass_label.setOpenExternalLinks(False)
        self.pass_label.setObjectName("pass_label")
        self.formLayoutLabels.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pass_label)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.formLayoutLabels)
        self.formLayoutLineEdit = QtWidgets.QFormLayout()
        self.formLayoutLineEdit.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.formLayoutLineEdit.setContentsMargins(-1, 6, -1, -1)
        self.formLayoutLineEdit.setObjectName("formLayoutLineEdit")
        self.user_line = QtWidgets.QLineEdit(self.LoginPage)
        self.user_line.setText("")
        self.user_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.user_line.setObjectName("user_line")
        self.formLayoutLineEdit.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.user_line)
        self.pass_line = QtWidgets.QLineEdit(self.LoginPage)
        self.pass_line.setText("")
        self.pass_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_line.setObjectName("pass_line")
        self.formLayoutLineEdit.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.pass_line)
        self.formLayout_3.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.formLayoutLineEdit)
        self.loginBtn = QtWidgets.QPushButton(self.LoginPage)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.loginBtn.setFont(font)
        self.loginBtn.setAutoDefault(True)
        self.loginBtn.setObjectName("loginBtn")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.loginBtn)
        StackedWidget.addWidget(self.LoginPage)

        self.retranslateUi(StackedWidget)
        QtCore.QMetaObject.connectSlotsByName(StackedWidget)

    def retranslateUi(self, StackedWidget):
        _translate = QtCore.QCoreApplication.translate
        StackedWidget.setWindowTitle(_translate("StackedWidget", "FUBC Library"))
        self.user_label.setText(_translate("StackedWidget", "User Name"))
        self.pass_label.setText(_translate("StackedWidget", "Password"))
        self.loginBtn.setText(_translate("StackedWidget", "Log In "))

