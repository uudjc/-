from PyQt5.QtGui import QPalette, QColor, QFont

from Login_ui import *
from control.login import LoginWindow
from view.mainwindow import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from control.mainWindow import MyWindow
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
import sys
from model.connectsqlite import ConnectSqlite
import model.configuration


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_LoginWindow()
#         self.ui.setupUi(self)
#         self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#         self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#         self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = LoginWindow()
    # main = MyWindow()
    sys.exit(app.exec_())
