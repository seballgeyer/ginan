# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)
from scripts.GinanUI.app.resources import ginan_logo_rc
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.headerLayout = QHBoxLayout()
        self.headerLayout.setObjectName(u"headerLayout")
        self.logoLabel = QLabel(self.centralwidget)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setMaximumSize(QSize(60, 60))
        self.logoLabel.setPixmap(QPixmap(u":/img/ginan-logo.png"))
        self.logoLabel.setScaledContents(True)

        self.headerLayout.addWidget(self.logoLabel)

        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.titleLabel.setFont(font)

        self.headerLayout.addWidget(self.titleLabel)


        self.verticalLayout.addLayout(self.headerLayout)

        self.mainContentLayout = QHBoxLayout()
        self.mainContentLayout.setObjectName(u"mainContentLayout")
        self.leftSidebarLayout = QVBoxLayout()
        self.leftSidebarLayout.setObjectName(u"leftSidebarLayout")
        self.leftSidebarLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.observationsButton = QPushButton(self.centralwidget)
        self.observationsButton.setObjectName(u"observationsButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.observationsButton.sizePolicy().hasHeightForWidth())
        self.observationsButton.setSizePolicy(sizePolicy)
        self.observationsButton.setMinimumSize(QSize(0, 40))
        self.observationsButton.setStyleSheet(u"QPushButton { \n"
"	background-color: rgb(24, 24, 24);\n"
"	selection-background-color: rgb(12, 17, 109);\n"
"	color: rgb(255, 255, 255);\n"
"	border-color: rgb(189, 189, 189);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"	background-color: rgb(89, 89, 89);\n"
"}")

        self.horizontalLayout.addWidget(self.observationsButton)

        self.outputButton = QPushButton(self.centralwidget)
        self.outputButton.setObjectName(u"outputButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.outputButton.sizePolicy().hasHeightForWidth())
        self.outputButton.setSizePolicy(sizePolicy1)
        self.outputButton.setMinimumSize(QSize(0, 40))
        self.outputButton.setMaximumSize(QSize(367, 16777215))
        self.outputButton.setStyleSheet(u"QPushButton { \n"
"	background-color: rgb(24, 24, 24);\n"
"	selection-background-color: rgb(12, 17, 109);\n"
"	color: rgb(255, 255, 255);\n"
"	border-color: rgb(189, 189, 189);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"	background-color: rgb(89, 89, 89);\n"
"}")

        self.horizontalLayout.addWidget(self.outputButton)


        self.leftSidebarLayout.addLayout(self.horizontalLayout)

        self.Constellations = QFrame(self.centralwidget)
        self.Constellations.setObjectName(u"Constellations")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Constellations.sizePolicy().hasHeightForWidth())
        self.Constellations.setSizePolicy(sizePolicy2)
        self.Constellations.setStyleSheet(u"background-color: rgb(24, 24, 24);\n"
"color: rgb(255, 255, 255);")
        self.Constellations.setFrameShape(QFrame.Shape.NoFrame)
        self.configGridLayout = QGridLayout(self.Constellations)
        self.configGridLayout.setObjectName(u"configGridLayout")
        self.configGridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.configGridLayout.setHorizontalSpacing(8)
        self.configGridLayout.setVerticalSpacing(10)
        self.configGridLayout.setContentsMargins(5, 5, 5, 5)
        self.receiverTypeValue = QLabel(self.Constellations)
        self.receiverTypeValue.setObjectName(u"receiverTypeValue")
        sizePolicy2.setHeightForWidth(self.receiverTypeValue.sizePolicy().hasHeightForWidth())
        self.receiverTypeValue.setSizePolicy(sizePolicy2)
        self.receiverTypeValue.setVisible(False)

        self.configGridLayout.addWidget(self.receiverTypeValue, 5, 3, 1, 1)

        self.antennaOffsetValue = QLineEdit(self.Constellations)
        self.antennaOffsetValue.setObjectName(u"antennaOffsetValue")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.antennaOffsetValue.sizePolicy().hasHeightForWidth())
        self.antennaOffsetValue.setSizePolicy(sizePolicy3)
        self.antennaOffsetValue.setVisible(False)
        self.antennaOffsetValue.setStyleSheet(u"background:transparent;border:none;")
        self.antennaOffsetValue.setReadOnly(True)

        self.configGridLayout.addWidget(self.antennaOffsetValue, 7, 3, 1, 1)

        self.receiveTypeLabel = QLabel(self.Constellations)
        self.receiveTypeLabel.setObjectName(u"receiveTypeLabel")

        self.configGridLayout.addWidget(self.receiveTypeLabel, 5, 0, 1, 1)

        self.dataIntervalLabel = QLabel(self.Constellations)
        self.dataIntervalLabel.setObjectName(u"dataIntervalLabel")

        self.configGridLayout.addWidget(self.dataIntervalLabel, 4, 0, 1, 1)

        self.antennaOffsetLabel = QLabel(self.Constellations)
        self.antennaOffsetLabel.setObjectName(u"antennaOffsetLabel")

        self.configGridLayout.addWidget(self.antennaOffsetLabel, 7, 0, 1, 1)

        self.dataIntervalValue = QLabel(self.Constellations)
        self.dataIntervalValue.setObjectName(u"dataIntervalValue")
        sizePolicy2.setHeightForWidth(self.dataIntervalValue.sizePolicy().hasHeightForWidth())
        self.dataIntervalValue.setSizePolicy(sizePolicy2)
        self.dataIntervalValue.setVisible(False)

        self.configGridLayout.addWidget(self.dataIntervalValue, 4, 3, 1, 1)

        self.pppSeriesLabel = QLabel(self.Constellations)
        self.pppSeriesLabel.setObjectName(u"pppSeriesLabel")

        self.configGridLayout.addWidget(self.pppSeriesLabel, 10, 0, 1, 1)

        self.pppSeriesValue = QLabel(self.Constellations)
        self.pppSeriesValue.setObjectName(u"pppSeriesValue")
        sizePolicy2.setHeightForWidth(self.pppSeriesValue.sizePolicy().hasHeightForWidth())
        self.pppSeriesValue.setSizePolicy(sizePolicy2)
        self.pppSeriesValue.setVisible(False)

        self.configGridLayout.addWidget(self.pppSeriesValue, 10, 3, 1, 1)

        self.showConfigValue = QLabel(self.Constellations)
        self.showConfigValue.setObjectName(u"showConfigValue")
        sizePolicy2.setHeightForWidth(self.showConfigValue.sizePolicy().hasHeightForWidth())
        self.showConfigValue.setSizePolicy(sizePolicy2)
        self.showConfigValue.setVisible(False)

        self.configGridLayout.addWidget(self.showConfigValue, 27, 0, 1, 1)

        self.antennaOffsetButton = QPushButton(self.Constellations)
        self.antennaOffsetButton.setObjectName(u"antennaOffsetButton")
        sizePolicy3.setHeightForWidth(self.antennaOffsetButton.sizePolicy().hasHeightForWidth())
        self.antennaOffsetButton.setSizePolicy(sizePolicy3)
        self.antennaOffsetButton.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.antennaOffsetButton, 7, 2, 1, 1)

        self.timeWindowValue = QLabel(self.Constellations)
        self.timeWindowValue.setObjectName(u"timeWindowValue")
        sizePolicy2.setHeightForWidth(self.timeWindowValue.sizePolicy().hasHeightForWidth())
        self.timeWindowValue.setSizePolicy(sizePolicy2)
        self.timeWindowValue.setVisible(False)

        self.configGridLayout.addWidget(self.timeWindowValue, 3, 3, 1, 1)

        self.timeWindowLabel = QLabel(self.Constellations)
        self.timeWindowLabel.setObjectName(u"timeWindowLabel")

        self.configGridLayout.addWidget(self.timeWindowLabel, 3, 0, 1, 1)

        self.antennaTypeValue = QLabel(self.Constellations)
        self.antennaTypeValue.setObjectName(u"antennaTypeValue")
        sizePolicy2.setHeightForWidth(self.antennaTypeValue.sizePolicy().hasHeightForWidth())
        self.antennaTypeValue.setSizePolicy(sizePolicy2)
        self.antennaTypeValue.setVisible(False)

        self.configGridLayout.addWidget(self.antennaTypeValue, 6, 3, 1, 1)

        self.antennaTypeLabel = QLabel(self.Constellations)
        self.antennaTypeLabel.setObjectName(u"antennaTypeLabel")

        self.configGridLayout.addWidget(self.antennaTypeLabel, 6, 0, 1, 1)

        self.pppProviderValue = QLabel(self.Constellations)
        self.pppProviderValue.setObjectName(u"pppProviderValue")
        sizePolicy2.setHeightForWidth(self.pppProviderValue.sizePolicy().hasHeightForWidth())
        self.pppProviderValue.setSizePolicy(sizePolicy2)
        self.pppProviderValue.setVisible(False)

        self.configGridLayout.addWidget(self.pppProviderValue, 8, 3, 1, 1)

        self.PPP_provider = QComboBox(self.Constellations)
        self.PPP_provider.addItem("")
        self.PPP_provider.setObjectName(u"PPP_provider")
        sizePolicy3.setHeightForWidth(self.PPP_provider.sizePolicy().hasHeightForWidth())
        self.PPP_provider.setSizePolicy(sizePolicy3)
        self.PPP_provider.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.PPP_provider, 8, 2, 1, 1)

        self.pppProviderLabel = QLabel(self.Constellations)
        self.pppProviderLabel.setObjectName(u"pppProviderLabel")

        self.configGridLayout.addWidget(self.pppProviderLabel, 8, 0, 1, 1)

        self.dataIntervalButton = QPushButton(self.Constellations)
        self.dataIntervalButton.setObjectName(u"dataIntervalButton")
        sizePolicy3.setHeightForWidth(self.dataIntervalButton.sizePolicy().hasHeightForWidth())
        self.dataIntervalButton.setSizePolicy(sizePolicy3)
        self.dataIntervalButton.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.dataIntervalButton, 4, 2, 1, 1)

        self.modeValue = QLabel(self.Constellations)
        self.modeValue.setObjectName(u"modeValue")
        self.modeValue.setVisible(False)

        self.configGridLayout.addWidget(self.modeValue, 1, 3, 1, 1)

        self.Receiver_type = QComboBox(self.Constellations)
        self.Receiver_type.addItem("")
        self.Receiver_type.setObjectName(u"Receiver_type")
        sizePolicy3.setHeightForWidth(self.Receiver_type.sizePolicy().hasHeightForWidth())
        self.Receiver_type.setSizePolicy(sizePolicy3)
        self.Receiver_type.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.Receiver_type, 5, 2, 1, 1)

        self.Antenna_type = QComboBox(self.Constellations)
        self.Antenna_type.addItem("")
        self.Antenna_type.setObjectName(u"Antenna_type")
        sizePolicy3.setHeightForWidth(self.Antenna_type.sizePolicy().hasHeightForWidth())
        self.Antenna_type.setSizePolicy(sizePolicy3)
        self.Antenna_type.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.Antenna_type, 6, 2, 1, 1)

        self.showConfigButton = QPushButton(self.Constellations)
        self.showConfigButton.setObjectName(u"showConfigButton")
        sizePolicy3.setHeightForWidth(self.showConfigButton.sizePolicy().hasHeightForWidth())
        self.showConfigButton.setSizePolicy(sizePolicy3)
        self.showConfigButton.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:2px 8px;font:13pt \"Segoe UI\";text-align:center;")

        self.configGridLayout.addWidget(self.showConfigButton, 27, 0, 1, 3)

        self.constellationsLabel = QLabel(self.Constellations)
        self.constellationsLabel.setObjectName(u"constellationsLabel")

        self.configGridLayout.addWidget(self.constellationsLabel, 2, 0, 1, 1)

        self.Constellations_2 = QComboBox(self.Constellations)
        self.Constellations_2.addItem("")
        self.Constellations_2.setObjectName(u"Constellations_2")
        sizePolicy3.setHeightForWidth(self.Constellations_2.sizePolicy().hasHeightForWidth())
        self.Constellations_2.setSizePolicy(sizePolicy3)
        self.Constellations_2.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.Constellations_2, 2, 2, 1, 1)

        self.timeWindowButton = QPushButton(self.Constellations)
        self.timeWindowButton.setObjectName(u"timeWindowButton")
        sizePolicy3.setHeightForWidth(self.timeWindowButton.sizePolicy().hasHeightForWidth())
        self.timeWindowButton.setSizePolicy(sizePolicy3)
        self.timeWindowButton.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.timeWindowButton, 3, 2, 1, 1)

        self.constellationsValue = QLabel(self.Constellations)
        self.constellationsValue.setObjectName(u"constellationsValue")
        self.constellationsValue.setVisible(False)

        self.configGridLayout.addWidget(self.constellationsValue, 2, 3, 1, 1)

        self.modeLabel = QLabel(self.Constellations)
        self.modeLabel.setObjectName(u"modeLabel")
        sizePolicy2.setHeightForWidth(self.modeLabel.sizePolicy().hasHeightForWidth())
        self.modeLabel.setSizePolicy(sizePolicy2)

        self.configGridLayout.addWidget(self.modeLabel, 1, 0, 1, 1)

        self.pppProjectLabel = QLabel(self.Constellations)
        self.pppProjectLabel.setObjectName(u"pppProjectLabel")
        self.pppProjectLabel.setMinimumSize(QSize(0, 0))
        self.pppProjectLabel.setMaximumSize(QSize(16777215, 16777215))

        self.configGridLayout.addWidget(self.pppProjectLabel, 12, 0, 1, 1)

        self.Mode = QComboBox(self.Constellations)
        self.Mode.addItem("")
        self.Mode.setObjectName(u"Mode")
        sizePolicy3.setHeightForWidth(self.Mode.sizePolicy().hasHeightForWidth())
        self.Mode.setSizePolicy(sizePolicy3)
        self.Mode.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.Mode, 1, 2, 1, 1)

        self.PPP_series = QComboBox(self.Constellations)
        self.PPP_series.addItem("")
        self.PPP_series.setObjectName(u"PPP_series")
        sizePolicy3.setHeightForWidth(self.PPP_series.sizePolicy().hasHeightForWidth())
        self.PPP_series.setSizePolicy(sizePolicy3)
        self.PPP_series.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.PPP_series, 10, 2, 1, 1)

        self.PPP_project = QComboBox(self.Constellations)
        self.PPP_project.addItem("")
        self.PPP_project.setObjectName(u"PPP_project")
        sizePolicy3.setHeightForWidth(self.PPP_project.sizePolicy().hasHeightForWidth())
        self.PPP_project.setSizePolicy(sizePolicy3)
        self.PPP_project.setStyleSheet(u"background-color:#2c5d7c;color:white;padding:0px 8px;font:13pt \"Segoe UI\";text-align:left;")

        self.configGridLayout.addWidget(self.PPP_project, 12, 2, 1, 1)


        self.leftSidebarLayout.addWidget(self.Constellations)

        self.processButton = QPushButton(self.centralwidget)
        self.processButton.setObjectName(u"processButton")
        sizePolicy.setHeightForWidth(self.processButton.sizePolicy().hasHeightForWidth())
        self.processButton.setSizePolicy(sizePolicy)
        self.processButton.setMinimumSize(QSize(0, 40))
        self.processButton.setStyleSheet(u"QPushButton { \n"
"	color:black;font-weight:bold;\n"
"	background-color: rgb(21, 134, 19);\n"
"	border-color: rgb(189, 189, 189);\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"	background-color: rgb(89, 89, 89);\n"
"}\n"
"\n"
"")

        self.leftSidebarLayout.addWidget(self.processButton)

        self.stopAllButton = QPushButton(self.centralwidget)
        self.stopAllButton.setObjectName(u"stopAllButton")
        self.stopAllButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.stopAllButton.setStyleSheet(u"\n"
"QPushButton { background-color: #d32f2f; color: white; font-weight: bold; }\n"
"QPushButton:hover { background-color: #b71c1c; }\n"
"QPushButton:pressed { background-color: #9a0007; }\n"
"QPushButton:disabled { background-color: rgb(120,120,120); }\n"
"            ")

        self.leftSidebarLayout.addWidget(self.stopAllButton)


        self.mainContentLayout.addLayout(self.leftSidebarLayout)

        self.rightLayout = QVBoxLayout()
        self.rightLayout.setObjectName(u"rightLayout")
        self.cddisCredentialsLayout = QHBoxLayout()
        self.cddisCredentialsLayout.setObjectName(u"cddisCredentialsLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.cddisCredentialsLayout.addItem(self.horizontalSpacer)

        self.cddisCredentialsButton = QPushButton(self.centralwidget)
        self.cddisCredentialsButton.setObjectName(u"cddisCredentialsButton")
        self.cddisCredentialsButton.setMinimumSize(QSize(150, 30))
        self.cddisCredentialsButton.setStyleSheet(u"background-color:#2c5d7c;\n"
"color:white;\n"
"padding:2px 8px;\n"
"font:13pt \"Segoe UI\";\n"
"text-align:center;")

        self.cddisCredentialsLayout.addWidget(self.cddisCredentialsButton)


        self.rightLayout.addLayout(self.cddisCredentialsLayout)

        self.workflowLabel = QLabel(self.centralwidget)
        self.workflowLabel.setObjectName(u"workflowLabel")
        font1 = QFont()
        font1.setPointSize(14)
        font1.setBold(True)
        self.workflowLabel.setFont(font1)

        self.rightLayout.addWidget(self.workflowLabel)

        self.terminalTextEdit = QTextEdit(self.centralwidget)
        self.terminalTextEdit.setObjectName(u"terminalTextEdit")
        self.terminalTextEdit.setStyleSheet(u"background-color:#2c5d7c;color:white;")
        self.terminalTextEdit.setReadOnly(True)

        self.rightLayout.addWidget(self.terminalTextEdit)

        self.visualisationLabel = QLabel(self.centralwidget)
        self.visualisationLabel.setObjectName(u"visualisationLabel")
        self.visualisationLabel.setFont(font1)

        self.rightLayout.addWidget(self.visualisationLabel)

        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.setObjectName(u"webEngineView")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.webEngineView.sizePolicy().hasHeightForWidth())
        self.webEngineView.setSizePolicy(sizePolicy4)
        self.webEngineView.setUrl(QUrl(u"about:blank"))

        self.rightLayout.addWidget(self.webEngineView)


        self.mainContentLayout.addLayout(self.rightLayout)


        self.verticalLayout.addLayout(self.mainContentLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"GINAN GNSS Processing", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"GINAN GNSS PROCESSING GUI", None))
        self.observationsButton.setText(QCoreApplication.translate("MainWindow", u"Observations", None))
        self.outputButton.setText(QCoreApplication.translate("MainWindow", u"Output", None))
        self.receiverTypeValue.setText(QCoreApplication.translate("MainWindow", u"Receiver type", None))
        self.antennaOffsetValue.setText(QCoreApplication.translate("MainWindow", u"Antenna offset", None))
        self.receiveTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Receiver type", None))
        self.dataIntervalLabel.setText(QCoreApplication.translate("MainWindow", u"Data Interval", None))
        self.antennaOffsetLabel.setText(QCoreApplication.translate("MainWindow", u"Antenna offset", None))
        self.dataIntervalValue.setText(QCoreApplication.translate("MainWindow", u"Data interval", None))
        self.pppSeriesLabel.setText(QCoreApplication.translate("MainWindow", u"PPP series", None))
        self.pppSeriesValue.setText(QCoreApplication.translate("MainWindow", u"PPP series", None))
        self.showConfigValue.setText(QCoreApplication.translate("MainWindow", u"Open Yaml config in editor", None))
        self.antennaOffsetButton.setText(QCoreApplication.translate("MainWindow", u"0.0, 0.0, 0.0", None))
        self.timeWindowValue.setText(QCoreApplication.translate("MainWindow", u"Time Window", None))
        self.timeWindowLabel.setText(QCoreApplication.translate("MainWindow", u"Time window", None))
        self.antennaTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Antenna type", None))
        self.pppProviderValue.setText(QCoreApplication.translate("MainWindow", u"PPP provider", None))
        self.PPP_provider.setItemText(0, QCoreApplication.translate("MainWindow", u"Select one", None))

        self.pppProviderLabel.setText(QCoreApplication.translate("MainWindow", u"PPP provider", None))
        self.dataIntervalButton.setText(QCoreApplication.translate("MainWindow", u"Interval (Seconds)", None))
        self.modeValue.setText(QCoreApplication.translate("MainWindow", u"Static", None))
        self.Receiver_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Import list", None))

        self.Antenna_type.setItemText(0, QCoreApplication.translate("MainWindow", u"Import list", None))

        self.showConfigButton.setText(QCoreApplication.translate("MainWindow", u"Show config", None))
        self.constellationsLabel.setText(QCoreApplication.translate("MainWindow", u"Constellations", None))
        self.Constellations_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Select one or more", None))

        self.timeWindowButton.setText(QCoreApplication.translate("MainWindow", u"Start/End", None))
        self.constellationsValue.setText(QCoreApplication.translate("MainWindow", u"Constellations", None))
        self.modeLabel.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.pppProjectLabel.setText(QCoreApplication.translate("MainWindow", u"PPP project", None))
        self.Mode.setItemText(0, QCoreApplication.translate("MainWindow", u"Select one", None))

        self.PPP_series.setItemText(0, QCoreApplication.translate("MainWindow", u"Select one", None))

        self.PPP_project.setItemText(0, QCoreApplication.translate("MainWindow", u"Select one", None))

        self.processButton.setText(QCoreApplication.translate("MainWindow", u"Process", None))
        self.stopAllButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.cddisCredentialsButton.setText(QCoreApplication.translate("MainWindow", u"CDDIS Credentials", None))
        self.workflowLabel.setText(QCoreApplication.translate("MainWindow", u"Workflow", None))
        self.terminalTextEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'.AppleSystemUIFont'; font-size:13pt;\">Pea output terminal</span></p></body></html>", None))
        self.visualisationLabel.setText(QCoreApplication.translate("MainWindow", u"Visualisation", None))
    # retranslateUi

