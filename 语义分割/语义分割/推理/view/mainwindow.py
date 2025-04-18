# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 960)

        MainWindow.setStyleSheet("background-color: rgb(250, 250, 250);border-radius: 10px;border: 1px solid #000000;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(300, 0, 1140, 960))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(0, 0, 300, 960))

        self.offset = None
        # 为 label_12 绑定鼠标事件
        self.label_12.mousePressEvent = self.mousePressEvent
        self.label_12.mouseMoveEvent = self.mouseMoveEvent


        font = QtGui.QFont()
        font.setFamily("Roboto")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color: rgb(69, 90, 100);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.label_12.setText("")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 20, 280, 100))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background-color: rgb(69, 90, 100);\n"
"color: rgb(255, 255, 255);")
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(90, 550, 71, 41))
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background-color: rgb(69, 90, 100);\n"
"color: rgb(255, 255, 255);")
        self.label_9.setObjectName("label_9")
        self.label_logo = QtWidgets.QLabel(self.centralwidget)
        self.label_logo.setGeometry(QtCore.QRect(500, 180, 800, 601))
        self.label_logo.setStyleSheet("border-image: url(:/icon/pic/logoface_3.png);")
        self.label_logo.setText("")
        self.label_logo.setObjectName("label_logo")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 200, 300, 600))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_register = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_register.sizePolicy().hasHeightForWidth())
        self.pushButton_register.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_register.setFont(font)
        self.pushButton_register.setStyleSheet("\n"
"QPushButton\n"
"{\n"
"    \n"
"    background-color: rgb(84, 110, 122);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   \n"
"    background-color: rgb(127, 154, 167);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover:pressed\n"
"{\n"
"    background-color:rgb(85,170,255);\n"
"    border:2px solid #3C80B1;\n"
"    border-radius:5px;\n"
"    color:white;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/pic/添加用户.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_register.setIcon(icon)
        self.pushButton_register.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_register.setObjectName("pushButton_register")
        self.verticalLayout_2.addWidget(self.pushButton_register)
        self.pushButton_checkin = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_checkin.sizePolicy().hasHeightForWidth())
        self.pushButton_checkin.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_checkin.setFont(font)
        self.pushButton_checkin.setStyleSheet("\n"
"QPushButton\n"
"{\n"
"    \n"
"    background-color: rgb(84, 110, 122);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   \n"
"    background-color: rgb(127, 154, 167);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover:pressed\n"
"{\n"
"    background-color:rgb(85,170,255);\n"
"    border:2px solid #3C80B1;\n"
"    border-radius:5px;\n"
"    color:white;\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/pic/checkin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_checkin.setIcon(icon1)
        self.pushButton_checkin.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_checkin.setObjectName("pushButton_checkin")
        self.verticalLayout_2.addWidget(self.pushButton_checkin)
        self.pushButton_checkin_record = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_checkin_record.sizePolicy().hasHeightForWidth())
        self.pushButton_checkin_record.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_checkin_record.setFont(font)
        self.pushButton_checkin_record.setStyleSheet("\n"
"QPushButton\n"
"{\n"
"    \n"
"    background-color: rgb(84, 110, 122);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   \n"
"    background-color: rgb(127, 154, 167);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover:pressed\n"
"{\n"
"    background-color:rgb(85,170,255);\n"
"    border:2px solid #3C80B1;\n"
"    border-radius:5px;\n"
"    color:white;\n"
"}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/pic/checkinrecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_checkin_record.setIcon(icon2)
        self.pushButton_checkin_record.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_checkin_record.setObjectName("pushButton_checkin_record")
        self.verticalLayout_2.addWidget(self.pushButton_checkin_record)
        self.pushButton_face_record = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_face_record.sizePolicy().hasHeightForWidth())
        self.pushButton_face_record.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_face_record.setFont(font)
        self.pushButton_face_record.setStyleSheet("\n"
"QPushButton\n"
"{\n"
"    \n"
"    background-color: rgb(84, 110, 122);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   \n"
"    background-color: rgb(127, 154, 167);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover:pressed\n"
"{\n"
"    background-color:rgb(85,170,255);\n"
"    border:2px solid #3C80B1;\n"
"    border-radius:5px;\n"
"    color:white;\n"
"}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/pic/facerecord.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_face_record.setIcon(icon3)
        self.pushButton_face_record.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_face_record.setObjectName("pushButton_face_record")
        self.verticalLayout_2.addWidget(self.pushButton_face_record)
        self.pushButton_users = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_users.sizePolicy().hasHeightForWidth())
        self.pushButton_users.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_users.setFont(font)
        self.pushButton_users.setStyleSheet("\n"
"QPushButton\n"
"{\n"
"    \n"
"    background-color: rgb(84, 110, 122);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   \n"
"    background-color: rgb(127, 154, 167);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover:pressed\n"
"{\n"
"    background-color:rgb(85,170,255);\n"
"    border:2px solid #3C80B1;\n"
"    border-radius:5px;\n"
"    color:white;\n"
"}")
        self.pushButton_users.setIcon(icon3)
        self.pushButton_users.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_users.setObjectName("pushButton_users")
        self.verticalLayout_2.addWidget(self.pushButton_users)
        self.pushButton_about = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_about.sizePolicy().hasHeightForWidth())
        self.pushButton_about.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_about.setFont(font)
        self.pushButton_about.setStyleSheet("\n"
"QPushButton\n"
"{\n"
"    \n"
"    background-color: rgb(84, 110, 122);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   \n"
"    background-color: rgb(127, 154, 167);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover:pressed\n"
"{\n"
"    background-color:rgb(85,170,255);\n"
"    border:2px solid #3C80B1;\n"
"    border-radius:5px;\n"
"    color:white;\n"
"}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/pic/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_about.setIcon(icon4)
        self.pushButton_about.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_about.setObjectName("pushButton_about")
        self.verticalLayout_2.addWidget(self.pushButton_about)
        self.pushButton_exit = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_exit.sizePolicy().hasHeightForWidth())
        self.pushButton_exit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("等线")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_exit.setFont(font)
        self.pushButton_exit.setStyleSheet("\n"
"QPushButton\n"
"{\n"
"    \n"
"    background-color: rgb(84, 110, 122);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"QPushButton:hover\n"
"{\n"
"   \n"
"    background-color: rgb(127, 154, 167);\n"
"\n"
"    border-radius:5px;\n"
"   \n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover:pressed\n"
"{\n"
"    background-color:rgb(85,170,255);\n"
"    border:2px solid #3C80B1;\n"
"    border-radius:5px;\n"
"    color:white;\n"
"}")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/pic/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_exit.setIcon(icon5)
        self.pushButton_exit.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.verticalLayout_2.addWidget(self.pushButton_exit)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def mousePressEvent(self, event):
            self.offset = event.pos()  # 记录鼠标相对于窗口的位置

    def mouseMoveEvent(self, event):
            if self.offset is not None:
                    # 计算窗口新位置
                    x = event.globalX() - self.offset.x()
                    y = event.globalY() - self.offset.y()
                    self.move(x, y)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "轨道语义分割系统"))
        self.label_8.setText(_translate("MainWindow", "轨道语义分割系统"))
        self.label_9.setText(_translate("MainWindow", ""))
        self.pushButton_register.setText(_translate("MainWindow", "  图片分割        "))
        self.pushButton_checkin.setText(_translate("MainWindow", "  视频分割        "))
        self.pushButton_checkin_record.setText(_translate("MainWindow", "  分割记录        "))
        self.pushButton_face_record.setText(_translate("MainWindow", "    数据库         "))
        self.pushButton_users.setText(_translate("MainWindow", "      用户            "))
        self.pushButton_about.setText(_translate("MainWindow", "      关于            "))
        self.pushButton_exit.setText(_translate("MainWindow", "      退出            "))
import resource_rc
