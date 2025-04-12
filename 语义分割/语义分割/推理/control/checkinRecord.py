

from view.checkinrecord  import*
from view.checkinmodify import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QAbstractItemView, QTableWidgetItem, QLabel, QDialog, QFileDialog
from model.connectsqlite import ConnectSqlite
import model.configuration
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class CheckInRecord(QWidget, Ui_CheckInRecordForm):

    def __init__(self, result,parent=None):
        super(CheckInRecord, self).__init__(parent)
        self.setupUi(self)
        # sqlite3 connect
        self.dbcon = ConnectSqlite(model.configuration.DATABASE_PATH)
        self.checkin_data = []
        self.pushButton_search.clicked.connect(self.search)
        self.pushButton_modify.clicked.connect(self.modify)
        self.pushButton_delete.clicked.connect(self.delete)
        self.pushButton_export.clicked.connect(self.export)
        if result == '0':
            # 隐藏按钮
            self.pushButton_modify.setVisible(False)
            self.pushButton_delete.setVisible(False)
            self.pushButton_export.setVisible(False)
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
            for i in self.checkin_data:
                if search_str.lower() in str(i[1]).lower():
                    search_result = str(i[1])
                    # 设置目标行
                    self.tableWidget.setCurrentIndex(self.tableWidget.model().index(row,1))
                if search_str.lower() in str(i[0]).lower():
                    search_result = str(i[0])
                    # 设置目标行
                    self.tableWidget.setCurrentIndex(self.tableWidget.model().index(row, 0))
                if search_str.lower() in str(i[2]).lower():
                    search_result = str(i[2])
                    # 设置目标行
                    self.tableWidget.setCurrentIndex(self.tableWidget.model().index(row, 2))
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
            name = str(self.checkin_data[row][1])
            sid = str(self.checkin_data[row][0])

            checkin_time = str(self.checkin_data[row][2])
            id = self.checkin_data[row][-1]
            insert_list = [name,sid,checkin_time]
            dialog = CheckInModify(insert_list)
            dialog.exec_()
            modify_list = dialog.getInputs()
            modify_flag = modify_list[1]
            print("iddddd{}".format(id))
            result = self.dbcon.update_checkin_table(modify_list[0],id)
            if modify_flag:
                if result == 0:
                    self.make_table()
                    reply = QMessageBox.information(self, 'Success', 'Modify succeed!',
                                                QMessageBox.Yes, QMessageBox.Yes)
                else:
                    reply = QMessageBox.warning(self, 'Error', result,
                                                QMessageBox.Yes, QMessageBox.Yes)

        else:
            reply = QMessageBox.warning(self, 'Error', 'Please select the Record need to modify!',
                                        QMessageBox.Yes, QMessageBox.Yes)
    #delete
    def delete(self):
        select = self.tableWidget.selectedItems()
        if len(select) != 0:
            row = self.tableWidget.selectedItems()[0].row()  # 获取选中文本所在的行
            column = self.tableWidget.selectedItems()[0].column()
            id = self.checkin_data[row][-1]
            result = self.dbcon.delete_checkin_table(id)
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

    def export(self):
        # 弹出文件夹选择对话框
        # folder_path = QFileDialog.getExistingDirectory(self, "选择保存文件夹")

        folder_path = QFileDialog.getExistingDirectory(self, "选择保存文件夹")

    # show  database the table
    def make_table(self):
        #clear the table
        self.tableWidget.clear()

        self.checkin_data = self.dbcon.return_all_checkin_record()
        data_show = []
        for row in self.checkin_data:
            name = row[1]
            student_id = str(row[0])
            checkin_time = row[2].split(".")[0]
            data_show.append([name,student_id,checkin_time])


        self.RowLength = 0
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setColumnWidth(0, 220)  # 设置1列的宽度
        self.tableWidget.setColumnWidth(1, 220)  # 设置2列的宽度
        self.tableWidget.setColumnWidth(2, 300)  # 设置3列的宽度


        self.tableWidget.setHorizontalHeaderLabels(["姓名", "学号","进入时间"])
        self.tableWidget.setRowCount(self.RowLength)
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.raise_()

        for row_data in data_show:
            # 显示表格
            self.RowLength = self.RowLength + 1
            label = QLabel()
            self.tableWidget.verticalHeader().setDefaultSectionSize(40)
            self.tableWidget.setRowCount(self.RowLength)
            self.tableWidget.setItem(self.RowLength - 1, 0, QTableWidgetItem(row_data[0]))
            self.tableWidget.setItem(self.RowLength - 1, 1, QTableWidgetItem(row_data[1]))
            self.tableWidget.setItem(self.RowLength - 1, 2, QTableWidgetItem(row_data[2]))  # str(result['Loc'])

            #self.tableWidget.setItem(self.RowLength - 1, 6, QTableWidgetItem(row_data[6]))

            self.tableWidget.item(self.RowLength - 1, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(self.RowLength - 1, 1).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.item(self.RowLength - 1, 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #self.tableWidget.item(self.RowLength - 1, 6).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #close
    def close_all(self):
        self.close()
## Check-in Record Modify Dialog
class CheckInModify(QDialog, Ui_Dialog):

    def __init__(self,current_list,parent=None):
        super(CheckInModify, self).__init__(parent)
        self.setupUi(self)
        self.name = current_list[0]
        self.sid = current_list[1]
        self.checkin_time = current_list[2]
        self.lineEdit_sno.setText(self.sid)
        self.lineEdit_name.setText(self.name)
        print(self.checkin_time)
        self.modify_flag = False
        time1 = int(self.checkin_time.split(' ')[1].split(':')[0])
        time2 = int(self.checkin_time.split(' ')[1].split(':')[1])
        time1_format = str('{:0>2d}'.format(time1))
        time2_format = str('{:0>2d}'.format(time2))
        self.timeEdit_checkin.setTime(QTime.fromString(time1_format + ':' + time2_format))
        self.pushButton_add.clicked.connect(self.modify_return)


    def modify_return(self):

            self.modify_flag = True
            self.close()
    def getInputs(self):
        name = self.lineEdit_name.text()
        sid = self.lineEdit_sno.text()

        checkin_time = self.checkin_time.split(' ')[0] + " " + self.timeEdit_checkin.text()
        return [[name,sid,checkin_time],self.modify_flag]