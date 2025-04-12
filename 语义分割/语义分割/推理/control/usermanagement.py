from view.facerecord import*
from view.facemodify import *
from PyQt5.QtWidgets import QWidget,QMessageBox,QAbstractItemView,QTableWidgetItem,QLabel,QDialog
from model.connectsqlite import ConnectSqlite
import model.configuration
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import cv2

from view.usermanagement import Ui_UserManagement
from view.usermodify import Ui_UserModifyDialog


class UserManagement(QWidget, Ui_UserManagement):

    def __init__(self, parent=None):
        super(UserManagement, self).__init__(parent)
        self.setupUi(self)
        # sqlite3 connect
        self.dbcon = ConnectSqlite(model.configuration.DATABASE_PATH)
        # self.face_data = []
        self.user_data = []
        self.pushButton_search.clicked.connect(self.search)
        self.pushButton_modify.clicked.connect(self.modify)
        self.pushButton_delete.clicked.connect(self.delete)
        self.make_table()
    #search
    def search(self):
        print("search")
        search_str = self.lineEdit_search.text()
        # 如果搜索框有数据
        row = 0
        search_result = None
        if search_str != '':
            # 遍历列表并查找
            for i in self.user_data:
                if search_str.lower() in str(i[0]).lower():
                    search_result = str(i[0])
                    # 设置目标行
                    self.tableWidget.setCurrentIndex(self.tableWidget.model().index(row,0))
                # if search_str.lower() in str(i[1]).lower():
                #     search_result = str(i[1])
                #     # 设置目标行
                #     self.tableWidget.setCurrentIndex(self.tableWidget.model().index(row, 1))
                row += 1
            if search_result == 0:
                reply = QMessageBox.warning(self, 'Error', 'No relevant information was found!',
                                            QMessageBox.Yes, QMessageBox.Yes)
        # 若搜索框没有数据，对话框提示
        else:
            reply = QMessageBox.warning(self, 'Error', 'Please input the search keywords',
                                        QMessageBox.Yes, QMessageBox.Yes)
    # modify
    def modify(self):

        select = self.tableWidget.selectedItems()
        if len(select) != 0:
            row = self.tableWidget.selectedItems()[0].row()  # 获取选中文本所在的行
            column = self.tableWidget.selectedItems()[0].column()
            print(row,column)

            username = str(self.user_data[row][0])
            password = str(self.user_data[row][1])
            role = str(self.user_data[row][2])
            role_name = '用户' if role == '0' else '管理员' if role == '1' else 'unknown'

            dialog = UserModify(username,password,role_name)
            dialog.exec_()

            modify_values = dialog.getInputs()
            modify_flag = modify_values[3]
            print(modify_values)
            modify_list = [modify_values[0],modify_values[1],modify_values[2]]

            result = self.dbcon.update_user_table(modify_list)
            if modify_flag:
                if result == 0:
                    self.make_table()
                    reply = QMessageBox.information(self, 'Success', 'Modify succeed!',
                                                QMessageBox.Yes, QMessageBox.Yes)
                else:
                    reply = QMessageBox.warning(self, 'Error', result,
                                                QMessageBox.Yes, QMessageBox.Yes)

        else:
            reply = QMessageBox.warning(self, 'Error', 'Please select the ID or Name need to modify!',
                                        QMessageBox.Yes, QMessageBox.Yes)
    #delete
    def delete(self):
        select = self.tableWidget.selectedItems()
        if len(select) != 0:
            row = self.tableWidget.selectedItems()[0].row()  # 获取选中文本所在的行
            column = self.tableWidget.selectedItems()[0].column()
            username = self.user_data[row][0]

            result = self.dbcon.delete_user_table(username)
            if result == 0:
                self.make_table()
                reply = QMessageBox.information(self, 'Success', 'Delete succeed!',
                                                QMessageBox.Yes, QMessageBox.Yes)
            else:
                reply = QMessageBox.warning(self, 'Error', result,
                                            QMessageBox.Yes, QMessageBox.Yes)

        else:
            reply = QMessageBox.warning(self, 'Error', 'Please select the data need to delete!',
                                        QMessageBox.Yes, QMessageBox.Yes)
    # show  database the table
    def make_table(self):
        #clear the table
        self.tableWidget.clear()

        self.user_data = self.dbcon.return_all_user()
        data_show = []
        for row in self.user_data:
            #print(row)
            username = row[0]
            password = row[1]
            # role = row[2]
            role = '用户' if row[2] == '0' else '管理员' if row[2] == '1' else 'unknown'
            data_show.append([username,password,role])

        #print(self.face_data)
        # 考勤记录-设置表格为5列，并为每一列设置宽度
        self.RowLength = 0
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0, 300)  # 设置1列的宽度
        self.tableWidget.setColumnWidth(1, 370)  # 设置2列的宽度
        self.tableWidget.setColumnWidth(2, 430)  # 设置3列的宽度

        self.tableWidget.setHorizontalHeaderLabels(["账号", "密码", "角色"])
        self.tableWidget.setRowCount(self.RowLength)
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.raise_()

        for row_data in data_show:
            # 显示表格
            self.RowLength = self.RowLength + 1
            label = QLabel()
            self.tableWidget.verticalHeader().setDefaultSectionSize(155)
            self.tableWidget.setRowCount(self.RowLength)
            self.tableWidget.setItem(self.RowLength - 1, 0, QTableWidgetItem(row_data[0]))
            self.tableWidget.setItem(self.RowLength - 1, 1, QTableWidgetItem(row_data[1]))
            self.tableWidget.setItem(self.RowLength - 1, 2, QTableWidgetItem(row_data[2]))  # str(result['Loc'])



            self.tableWidget.item(self.RowLength - 1, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(self.RowLength - 1, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(self.RowLength - 1, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    #close
    def close_all(self):
        self.close()

##Face Record Modify Dialog
class UserModify(QDialog, Ui_UserModifyDialog):

    def __init__(self, username,password,role,parent=None):
        super(UserModify, self).__init__(parent)
        self.setupUi(self)
        self.username = username
        self.password = password
        self.role = role

        self.lineEdit_name.setText(self.username)
        self.lineEdit_sno.setText(self.password)
        self.comboBox.setCurrentText(self.role)
        print(self.role)

        self.modify_flag = False

        self.pushButton_add.clicked.connect(self.modify_return)

    def modify_return(self):
        if self.lineEdit_sno.text() == self.password and self.lineEdit_name.text() == self.username and self.comboBox.currentText()==self.role:
            reply = QMessageBox.warning(self, 'Error', 'Not Modify!',
                                        QMessageBox.Yes, QMessageBox.Yes)

        else:
            self.modify_flag = True
            self.close()

    def getInputs(self):
        return (self.lineEdit_name.text(),self.lineEdit_sno.text(),self.comboBox.currentText(),self.modify_flag)

