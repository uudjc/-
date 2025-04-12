from view.facecheck import*
from PyQt5.QtWidgets import QWidget,QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model.connectsqlite import ConnectSqlite
import model.configuration
from model.checkin import find_current_course
from datetime import datetime
import cv2
import time
class FaceCheckin(QWidget, Ui_FaceCheckForm):

    def __init__(self, re,parent=None):
        super(FaceCheckin, self).__init__(parent)
        self.setupUi(self)
        # show the current time
        self.timer = QBasicTimer()  # QTimer()
        self.timer.start(1000, self)
        self.label_current.setText(time.strftime("%X", time.localtime()))

        self.CAM_OPEN_FLAG = False
        # recognize model
        self.re = re
        # sqlite3 connect
        self.dbcon = ConnectSqlite(model.configuration.DATABASE_PATH)
        self.student_info_all = self.dbcon.load_registered_data()

        # connect the pushbutton and function
        self.pushButton_open.clicked.connect(self.open_cam)
        self.pushButton_stop.clicked.connect(self.stop_cam)
        self.pushButton_checkin.clicked.connect(self.check_in)
        self.label_open.setVisible(False)

        self.timer_close = QTimer()
        self.timer_close.timeout.connect(self.close_door)

    # open the camera
    def open_cam(self):
        if not self.CAM_OPEN_FLAG:
            self.timer_camera = QTimer()  # 定义定时器
            # opencv read the camera
            self.cap = cv2.VideoCapture(0)
            # create the QTimer to show the frame
            self.timer_camera.start(10)
            self.timer_camera.timeout.connect(self.show_frame)
            self.CAM_OPEN_FLAG = True
        else:
            # show messegebox
            reply = QMessageBox.warning(self, 'Error', 'The camera is opened!',
                                        QMessageBox.Yes, QMessageBox.Yes)
    # stop the camera
    def stop_cam(self):
        if self.CAM_OPEN_FLAG:
            # stop the QTmer
            self.timer_camera.stop()
            # clear the label
            self.label_frame.clear()
            # release the camera
            self.cap.release()
            # turn off the flag
            self.CAM_OPEN_FLAG = False
        else:
            # show messegebox
            reply = QMessageBox.warning(self, 'Error', 'The camera is not opened!',
                                        QMessageBox.Yes, QMessageBox.Yes)
    #show the label on the frame
    def show_label(self,frame,label):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换为RGB图像
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = bytesPerComponent * width
        q_image = QImage(frame.data, width, height, bytesPerLine,  # 将图片转换为QImage格式
                         QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(q_image))
        label.setScaledContents(True)  # 拉伸铺满label
    # show the frame on the label
    def show_frame(self):
        if (self.cap.isOpened()):
            ret, self.frame = self.cap.read()
            if ret:
                self.show_label(self.frame, self.label_frame)
    # check in button
    def check_in(self):
        self.lineEdit_sno.setText("")
        self.lineEdit_name.setText("")
        self.progressBar.setValue(0)
        self.label_face.setPixmap(QPixmap(""))
        self.lineEdit_checkin_time.setText("")
        self.label_open.setVisible(False)
        self.timer_close.stop()


        if self.CAM_OPEN_FLAG:
            result,frame_photo,search_result = self.re.check_in(self.frame,self.student_info_all)
            if result == 0:
                # show messegebox
                reply = QMessageBox.warning(self, 'Error', 'No face detected!',
                                            QMessageBox.Yes, QMessageBox.Yes)
            elif result == 1:
                if search_result[2] >= model.configuration.SIMILARITY_THRESHOLD:  # 若相似度大于阀值
                    self.label_open.setVisible(True)
                    self.timer_close.start(5000)
                    self.lineEdit_sno.setText(str(search_result[0]))
                    self.lineEdit_name.setText(str(search_result[1]))
                    self.progressBar.setValue(search_result[2])
                    self.show_label(frame_photo, self.label_face)
                    self.lineEdit_checkin_time.setText(time.strftime("%X", time.localtime()))
                    change_time = datetime.now().strftime( '%Y/%m/%d %H:%M' )
                    #写入数据库
                    insert_list = [str(search_result[0]),str(search_result[1]),change_time]
                    save_result = self.dbcon.insert_checkin_table(insert_list)
                    if save_result != 0:
                        # show messegebox
                        reply = QMessageBox.warning(self, 'Error', 'Write to the database Failed!\n' + save_result,
                                                    QMessageBox.Yes, QMessageBox.Yes)

                else:
                    # show messegebox
                    self.show_label(frame_photo, self.label_face)
                    reply = QMessageBox.warning(self, '人脸识别失败', '识别失败！人脸未注册或者人脸相似度过低，请重试！',
                                                QMessageBox.Yes, QMessageBox.Yes)

        else:
            # show messegebox
            reply = QMessageBox.warning(self, 'Error', 'Please open the camera firstly!',
                                        QMessageBox.Yes, QMessageBox.Yes)
    #set the current time
    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.label_current.setText(time.strftime("%X", time.localtime()))
    # close the window
    def close_all(self):
        if self.CAM_OPEN_FLAG:
            # stop the QTmer
            self.timer_camera.stop()
            self.cap.release()
        self.close()

    def close_door(self):
        self.label_open.setVisible(False)
        self.timer_close.stop()
        self.lineEdit_sno.setText("")
        self.lineEdit_name.setText("")
        self.progressBar.setValue(0)
        self.label_face.setPixmap(QPixmap(""))

        self.lineEdit_checkin_time.setText("")