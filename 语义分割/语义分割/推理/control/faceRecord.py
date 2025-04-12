from view.facerecord import*
from view.facemodify import *
from PyQt5.QtWidgets import QWidget,QMessageBox,QAbstractItemView,QTableWidgetItem,QLabel,QDialog
from model.connectsqlite import ConnectSqlite
import model.configuration
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import cv2

class FaceRecord(QWidget, Ui_FaceRecordForm):

    def __init__(self,account1, result1,parent=None):
        super(FaceRecord, self).__init__(parent)
        self.account1 = account1
        self.result1 = result1
        self.setupUi(self)
        # sqlite3 connect
        self.dbcon = ConnectSqlite(model.configuration.DATABASE_PATH)
        self.face_data = []
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
            for i in self.face_data:
                if search_str.lower() in str(i[1]).lower():
                    search_result = str(i[1])
                    # 设置目标行
                    self.tableWidget.setCurrentIndex(self.tableWidget.model().index(row,0))
                if search_str.lower() in str(i[5]).lower():
                    search_result = str(i[5])
                    # 设置目标行
                    self.tableWidget.setCurrentIndex(self.tableWidget.model().index(row, 1))
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
            name = str(self.face_data[row][1])
            sid = str(self.face_data[row][5])
            id = self.face_data[row][0]
            dialog = FaceModify(name,sid)
            dialog.exec_()
            modify_values = dialog.getInputs()
            modify_flag = modify_values[2]
            print(modify_values)
            modify_list = [modify_values[0],modify_values[1],id]
            result = self.dbcon.update_face_table(modify_list)
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
            id = self.face_data[row][0]

            result = self.dbcon.delete_face_table(id)
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
        font = QFont("宋体", 10)  # 设置字体为宋体，字号为 10
        self.tableWidget.setFont(font)
        self.face_data = self.dbcon.return_all_face(self.account1,self.result1)

        data_show = []
        for row in self.face_data:
            print(row[1],'=============')
            id = row[0]
            name = str(row[1])
            student_id = str(row[5])
            # face_data = list(map(float, row[2].split('\n')))
            face_data = row[2]

            register_time = row[4].split('.')[0]
            face_photo = row[3]
            data_show.append([name,student_id,str(face_data),register_time,face_photo,id])

        #print(self.face_data)
        # 考勤记录-设置表格为5列，并为每一列设置宽度
        self.RowLength = 0
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setColumnWidth(0, 200)  # 设置1列的宽度
        self.tableWidget.setColumnWidth(1, 200)  # 设置2列的宽度
        self.tableWidget.setColumnWidth(2, 200)  # 设置3列的宽度
        self.tableWidget.setColumnWidth(3, 200)  # 设置4列的宽度
        self.tableWidget.setColumnWidth(4, 300)  # 设置5列的宽度

        self.tableWidget.setHorizontalHeaderLabels(["用户", "方式", "路径", "时间", "分割结果"])
        self.tableWidget.setRowCount(self.RowLength)
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.raise_()

        for row_data in data_show:
            # 显示表格
            self.RowLength = self.RowLength + 1
            print(type(row_data[4]))
            label = QLabel()
            self.tableWidget.verticalHeader().setDefaultSectionSize(155)
            self.tableWidget.setRowCount(self.RowLength)
            self.tableWidget.setItem(self.RowLength - 1, 0, QTableWidgetItem(row_data[0]))
            self.tableWidget.setItem(self.RowLength - 1, 1, QTableWidgetItem(row_data[1]))
            self.tableWidget.setItem(self.RowLength - 1, 2, QTableWidgetItem(row_data[2]))  # str(result['Loc'])
            self.tableWidget.setItem(self.RowLength - 1, 3, QTableWidgetItem(row_data[3]))
            label.setText(row_data[4])
            label.setScaledContents(True)  # 拉伸铺满label
            self.tableWidget.setCellWidget(self.RowLength -1,4,label)
            self.tableWidget.item(self.RowLength - 1, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(self.RowLength - 1, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(self.RowLength - 1, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(self.RowLength - 1, 3).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #self.tableWidget.item(self.RowLength - 1, 4).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #show the label on the frame
    def image_2_qicon(self,frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换为RGB图像
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = bytesPerComponent * width
        q_image = QImage(frame.data, width, height, bytesPerLine,  # 将图片转换为QImage格式
                         QImage.Format_RGB888)
        icon = QPixmap.fromImage(q_image)
        return icon
    #close
    def close_all(self):
        self.close()

##Face Record Modify Dialog
class FaceModify(QDialog, Ui_faceModifyDialog):

    def __init__(self, name,sid,parent=None):
        super(FaceModify, self).__init__(parent)
        self.setupUi(self)
        self.name = name
        self.sid = sid
        self.lineEdit_sno.setText(self.sid)
        self.lineEdit_name.setText(self.name)
        self.modify_flag = False
        self.pushButton_modify_2.clicked.connect(self.modify_return)

    def modify_return(self):
        if self.lineEdit_sno.text() == self.sid and self.lineEdit_name.text() == self.name:
            reply = QMessageBox.warning(self, 'Error', 'Not Modify!',
                                        QMessageBox.Yes, QMessageBox.Yes)

        else:
            self.modify_flag = True
            self.close()

    def getInputs(self):
        return (self.lineEdit_sno.text(),self.lineEdit_name.text(),self.modify_flag)

