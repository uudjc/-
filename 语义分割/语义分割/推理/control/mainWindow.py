#-*- coding:utf-8 -*-
from control.usermanagement import UserManagement
from main import  SemanticSegmentation_Img_App
from main1 import SemanticSegmentation_Vedio_App
from view.mainwindow import*
from control.faceRegister import FaceRegister
from control.faceCheckin import FaceCheckin
from control.faceRecord import FaceRecord
from control.checkinRecord import CheckInRecord
from PyQt5.QtWidgets import QMainWindow
import model.configuration

import sys

class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, result, account,parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        #connect the button and function
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_register.clicked.connect(self.face_register)
        self.pushButton_checkin.clicked.connect(self.check_in)
        self.pushButton_face_record.clicked.connect(self.face_record)
        self.pushButton_users.clicked.connect(self.user_management)
        self.pushButton_checkin_record.clicked.connect(self.check_in_record)
        self.pushButton_about.clicked.connect(self.about)
        self.pushButton_exit.clicked.connect(self.exit)
        # 保存传入的参数 result
        self.result = result
        self.account = account
        print(result)
        print(account)
        if result == '0':
            # 隐藏按钮
            # self.pushButton_face_record.setVisible(False)
            self.pushButton_users.setVisible(False)

        self.pushButton_checkin_record.setVisible(False)
    #face register  人脸注册
    def face_register(self):
        try:
            self.close_logo()
            for i in range(self.verticalLayout.count()):
                self.verticalLayout.itemAt(i).widget().close_all()
            self.verticalLayout.addWidget(SemanticSegmentation_Img_App(self.account))
        except Exception as e:
            print(f"face_register 函数出现异常: {e}")

    #check-in 人脸签到
    def check_in(self):
        try:
            self.close_logo()
            for i in range(self.verticalLayout.count()):
                self.verticalLayout.itemAt(i).widget().close_all()
            self.verticalLayout.addWidget(SemanticSegmentation_Vedio_App(self.account))
        except Exception as e:
            print(f"check_in 函数出现异常: {e}")

    #face record 人脸记录 打卡记录
    def face_record(self):
        try:
            self.close_logo()
            for i in range(self.verticalLayout.count()):
                self.verticalLayout.itemAt(i).widget().close_all()
            print(self.account,self.result,'1111111')
            self.verticalLayout.addWidget(FaceRecord(self.account,self.result))
        except Exception as e:
            print(f"face_record 函数出现异常: {e}")

    #  user_management  用户管理
    def user_management(self):
        try:
            self.close_logo()
            for i in range(self.verticalLayout.count()):
                self.verticalLayout.itemAt(i).widget().close_all()
            self.verticalLayout.addWidget(UserManagement())
        except Exception as e:
            print(f"user_management 函数出现异常: {e}")

    #check in record 打卡记录
    def check_in_record(self):
        try:
            self.close_logo()
            for i in range(self.verticalLayout.count()):
                self.verticalLayout.itemAt(i).widget().close_all()
            self.verticalLayout.addWidget(CheckInRecord(self.result))
        except Exception as e:
            print(f"check_in_record 函数出现异常: {e}")

    #about关于
    def about(self):
        try:
            for i in range(self.verticalLayout.count()):
                self.verticalLayout.itemAt(i).widget().close_all()
            self.label_logo.setVisible(True)
        except Exception as e:
            print(f"about 函数出现异常: {e}")

    #exit退出
    def exit(self):
        try:
            self.close()
            self.open_login_window()  # 打开登录窗口
        except Exception as e:
            print(f"exit 函数出现异常: {e}")

    def open_login_window(self):
        try:
            # 创建并显示登录窗口
            from control.login import LoginWindow

            self.login_window = LoginWindow()
            self.login_window.show()
        except Exception as e:
            print(f"open_login_window 函数出现异常: {e}")

    #close the welcome logo
    def close_logo(self):
        try:
            self.label_logo.setVisible(False)
        except Exception as e:
            print(f"close_logo 函数出现异常: {e}")
