# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 341)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.layoutGridRoot = QGridLayout()
        self.layoutGridRoot.setObjectName(u"layoutGridRoot")
        self.dynamicTabWidget = QTabWidget(self.centralwidget)
        self.dynamicTabWidget.setObjectName(u"dynamicTabWidget")
        self.defaultTab = QWidget()
        self.defaultTab.setObjectName(u"defaultTab")
        self.gridLayout_5 = QGridLayout(self.defaultTab)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.tabGridLayout = QGridLayout()
        self.tabGridLayout.setObjectName(u"tabGridLayout")

        self.gridLayout_5.addLayout(self.tabGridLayout, 0, 0, 1, 1)

        self.dynamicTabWidget.addTab(self.defaultTab, "")

        self.layoutGridRoot.addWidget(self.dynamicTabWidget, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.layoutGridRoot, 0, 0, 1, 1)

        self.logTextEdit = QPlainTextEdit(self.centralwidget)
        self.logTextEdit.setObjectName(u"logTextEdit")
        self.logTextEdit.setEnabled(True)
        self.logTextEdit.setReadOnly(True)

        self.gridLayout_3.addWidget(self.logTextEdit, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.dynamicTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.dynamicTabWidget.setTabText(self.dynamicTabWidget.indexOf(self.defaultTab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.logTextEdit.setPlainText("")
    # retranslateUi

