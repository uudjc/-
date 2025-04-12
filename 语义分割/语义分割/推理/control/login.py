from PyQt5.QtGui import QPalette, QColor, QFont

from Login_ui import *
from control.mainWindow import MyWindow
from view.mainwindow import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import sys
from model.connectsqlite import ConnectSqlite
import model.configuration

class LoginWindow(QMainWindow):
    dialog_signal = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.dbcon = ConnectSqlite(model.configuration.DATABASE_PATH)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(3,0)
        self.shadow.setBlurRadius(10)
        self.shadow.setColor(QtCore.Qt.gray)
        self.ui.frame.setGraphicsEffect(self.shadow)
        self.ui.pushButton_3.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_2.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.Login_button.clicked.connect(self.login_in)
        self.ui.Sign_button.clicked.connect(self.Sign_in)
        self.show()

    def Sign_in(self):
        account = self.ui.Sign_account.text()
        password = self.ui.Sign_password.text()
        password_sure = self.ui.Sign_passwordsure.text()
        if password != password_sure:
            self.showCustomMessageBox('两次密码输入不一致')
        else:
            result = self.dbcon.register_user(account,password)
            self.showCustomMessageBox(result)

    def login_in(self):
        account = self.ui.login_account.text()
        password = self.ui.login_password.text()
        result = self.dbcon.login_user(account,password)
        #默认登录密码
        if result == "0" or result == "1":
        #     self.dialog_signal.signatures(True)
        # else:
        #     self.dialog_signal.emit(False)  # 如果登录失败，发送False信号
            try:
                self.win = MyWindow(result,account)  # 创建MyWindow实例
                self.close()  # 关闭当前的LoginWindow
                self.win.show()
            except Exception as e:
                print(f"Error starting MyWindow: {e}")
                # 可以在这里弹出一个错误对话框告知用户登录后窗口启动失败
        else:
            print("Error", "Wrong account or password!")
            self.showCustomMessageBox(result)

    def showCustomMessageBox(self,text):
        # 创建一个 QMessageBox 实例
        msg = QMessageBox(self)

        # 设置图标为警告
        msg.setIcon(QMessageBox.Warning)
        msg.setText(text)
        msg.setWindowTitle("警告")

        # 自定义按钮
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        # 修改按钮样式
        button_ok = msg.button(QMessageBox.Ok)
        button_cancel = msg.button(QMessageBox.Cancel)

        button_ok.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border-radius: 12px;
                padding: 10px 20px;
                border: none;
                box-shadow: 0 4px 8px rgba(0, 128, 0, 0.3);
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        button_cancel.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-size: 16px;
                border-radius: 12px;
                padding: 10px 20px;
                border: none;
                box-shadow: 0 4px 8px rgba(255, 0, 0, 0.3);
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)

        # 设置字体
        font = QFont("Arial", 12)
        msg.setFont(font)

        # 设置弹窗背景色和字体颜色
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))  # 背景色
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))  # 文字颜色
        msg.setPalette(palette)

        # 设置弹窗样式：背景颜色，圆角，阴影
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #f5f5f5;
                border-radius: 15px;
                border: 2px solid #d3d3d3;
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            }
        """)

        # 显示弹窗
        msg.resize(400, 200)
        msg.exec_()