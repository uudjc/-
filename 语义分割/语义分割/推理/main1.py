import sys
import time
from datetime import datetime
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtGui import QPainter, QImage, QPixmap, QIcon
import cv2
import torch
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QFileDialog, QComboBox,
    QHBoxLayout, QMessageBox, QGridLayout, QDialog, QLineEdit
)
from mmseg.visualization import SegLocalVisualizer
from PIL import Image
from mmseg.apis import init_model, inference_model, show_result_pyplot
from torchvision import transforms
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# 检查 GPU 可用性
from model import configuration
from model.connectsqlite import ConnectSqlite
import model

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"[INFO] 使用设备: {device}")

config_path = "../mmseg_test_rs19/mmseg_test_rs19/configs/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024.py"
checkpoint_path = "../mmseg_test_rs19/mmseg_test_rs19/ckpts/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024-6660edec.pth"
model1 = init_model(config_path, checkpoint_path)
target_class = 17
background_class = 0
seg_local_visualizer = SegLocalVisualizer(
    vis_backends=[dict(type='LocalVisBackend')],
    alpha=0.5)

import os
import shutil

import mmcv
import cv2
import os

import mmcv
import cv2
import os
from datetime import datetime



def clear_folder(folder_path):
    # 确保目标文件夹存在
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        # 遍历文件夹内的所有文件
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path):  # 如果是文件就删除
                    os.remove(file_path)
                elif os.path.isdir(file_path):  # 如果是文件夹就递归删除
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"无法删除文件 {file_path}: {e}")
    else:
        print(f"文件夹 {folder_path} 不存在或不是文件夹。")



class InferenceThread(QThread):
    result_ready = pyqtSignal(QPixmap)

    def __init__(self, frame, algorithm, opacity, model1, target_class, background_class, current_frame):
        super().__init__()
        self.frame = frame
        self.algorithm = algorithm
        self.opacity = opacity
        self.model1 = model1
        self.target_class = target_class
        self.background_class = background_class
        self.current_frame = current_frame

    def run(self):
        try:
            if self.opacity < 0 or self.opacity > 1:
                raise ValueError
        except ValueError:
            return

        result = inference_model(self.model1, self.frame)
        if self.algorithm == '全种类分割':
            seg_mask = show_result_pyplot(self.model1, self.frame, result,withLabels = False, opacity=self.opacity,
                                          out_file=f"val_segmaps/temp{self.current_frame}.png",
                                          show=False)

        elif self.algorithm == '铁道分割':
            seg_pred = result.pred_sem_seg.data.cpu().numpy().squeeze()

            seg_pred[seg_pred != self.target_class] = self.background_class

            result.pred_sem_seg.data = seg_pred
            seg_mask = show_result_pyplot(self.model1, self.frame, result,withLabels = False, opacity=self.opacity,
                                          out_file=f"val_segmaps/temp{self.current_frame}.png",
                                          show=False)
#加我微信吧 18849054606   后续有需要直接找我
        # 加载并显示分割结果
        seg_image_path = f"val_segmaps/temp{self.current_frame}.png"
        seg_pixmap = QPixmap(seg_image_path)
        if not seg_pixmap.isNull():
            self.result_ready.emit(seg_pixmap)


class SemanticSegmentation_Vedio_App(QMainWindow):
    def __init__(self, account, parent=None):
        super().__init__(parent)
        self.account = account
        self.initUI()
        self.video_path = None
        self.evaluation_thread = None
        self.dbcon = ConnectSqlite(configuration.DATABASE_PATH)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video_frame)
        self.cap = None
        self.is_paused = False
        self.frames_to_skip = 50  # 默认快进/快退帧数
        self.processing_thread = None
        self.frame_count = 0
        self.inference_thread = None
        self.output_video_path = None

    def initUI(self):
        # 主窗口设置
        self.setWindowTitle('图像质量评估系统')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #2c2c2c; color: white;")

        # 中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 视频和结果显示区域
        display_layout = QHBoxLayout()
        display_layout.setSpacing(20)

        # 视频显示区域
        self.video_display = QLabel()
        self.video_display.setStyleSheet("border: 2px solid #444; border-radius: 10px;")
        # 设置固定大小
        self.video_display.setFixedSize(500, 400)
        display_layout.addWidget(self.video_display)

        # 处理结果显示区域
        self.result_display = QLabel()
        self.result_display.setStyleSheet("border: 2px solid #444; border-radius: 10px;")
        # 设置固定大小
        self.result_display.setFixedSize(500, 400)
        display_layout.addWidget(self.result_display)

        main_layout.addLayout(display_layout)

        # 操作按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        # 选择视频按钮
        self.select_btn = QPushButton(QIcon('folder.png'), '选择视频')
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.select_btn.clicked.connect(self.select_video)
        button_layout.addWidget(self.select_btn)

        # 算法选择下拉框
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.currentIndexChanged.connect(self.on_algorithm_selected)

        self.algorithm_combo.addItems(['全种类分割', '铁道分割'])
        self.algorithm_combo.setStyleSheet("""
            QComboBox {
                background-color: #444;
                color: white;
                padding: 8px;
                border: 1px solid #666;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox:hover {
                border-color: #888;
            }
        """)
        self.algorithm_combo.currentIndexChanged.connect(self.on_algorithm_selected)
        button_layout.addWidget(self.algorithm_combo)

        # 透明度标签
        opacity_label = QLabel("透明度：")
        button_layout.addWidget(opacity_label)

        # 不透明度输入框
        self.opacity_input = QLineEdit()
        self.opacity_input.setPlaceholderText("输入不透明度 (0-1)")
        self.opacity_input.setText("1")  # 设置默认值为 1
        self.opacity_input.setStyleSheet("""
            QLineEdit {
                background-color: #444;
                color: white;
                padding: 8px;
                border: 1px solid #666;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #888;
            }
        """)
        button_layout.addWidget(self.opacity_input)

        # 采样间隔标签
        interval_label = QLabel("采样间隔（帧）：")
        button_layout.addWidget(interval_label)

        # 间隔帧数输入框
        self.interval_input = QLineEdit()
        self.interval_input.setPlaceholderText("输入间隔帧数 (整数)")
        self.interval_input.setText(str(60))
        self.interval_input.setStyleSheet("""
              QLineEdit {
                  background-color: #444;
                  color: white;
                  padding: 8px;
                  border: 1px solid #666;
                  border-radius: 5px;
                  font-size: 14px;
              }
              QLineEdit:hover {
                  border-color: #888;
              }
          """)
        button_layout.addWidget(self.interval_input)

        # 评估按钮
        self.evaluate_btn = QPushButton(QIcon('run.png'), '开始评估')
        self.evaluate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.evaluate_btn.clicked.connect(self.evaluate_video)
        button_layout.addWidget(self.evaluate_btn)

        # 暂停/播放按钮
        self.pause_play_btn = QPushButton(QIcon('pause.png'), '暂停')
        self.pause_play_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #FFA000;
            }
        """)
        self.pause_play_btn.clicked.connect(self.pause_play_video)
        button_layout.addWidget(self.pause_play_btn)

        # 快进按钮
        self.forward_btn = QPushButton(QIcon('forward.png'), '快进')
        self.forward_btn.setStyleSheet("""
            QPushButton {
                background-color: #E91E63;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #C2185B;
            }
        """)
        self.forward_btn.clicked.connect(self.forward_video)
        button_layout.addWidget(self.forward_btn)

        # 快退按钮
        self.backward_btn = QPushButton(QIcon('backward.png'), '快退')
        self.backward_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        self.backward_btn.clicked.connect(self.backward_video)
        button_layout.addWidget(self.backward_btn)

        main_layout.addLayout(button_layout)

    def generate_video_from_images_with_mmcv_and_cv2(self,image_folder, frame_rate=30):
        # 获取当前时间并生成视频文件名
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        self.output_video_path = f'mv/output_video_{current_time}.mp4'

        # 获取文件夹中的所有图片文件
        images = [f for f in os.listdir(image_folder) if f.endswith('.png')]

        # 对文件按名称排序，确保按顺序生成视频
        images.sort()

        # 读取第一张图片，获取视频的帧大小
        first_image_path = os.path.join(image_folder, images[0])
        first_image = mmcv.imread(first_image_path)
        height, width, _ = first_image.shape

        # 创建 VideoWriter 对象
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 视频编码
        video_writer = cv2.VideoWriter(self.output_video_path, fourcc, frame_rate, (width, height))

        # 将每张图片添加到视频中
        for image_name in images:
            image_path = os.path.join(image_folder, image_name)
            image = mmcv.imread(image_path)
            video_writer.write(image)

        # 释放 VideoWriter 对象
        video_writer.release()
        print(f"视频已保存到 {self.output_video_path}")

    def on_algorithm_selected(self, index):
        algorithm = self.algorithm_combo.currentText()
        print(f"[INFO] 选择的算法：{algorithm}")

    def select_video(self):
        # 打开文件选择对话框
        options = QFileDialog.Options()
        path, _ = QFileDialog.getOpenFileName(
            self, "选择视频", "", "Video Files (*.mp4 *.avi)", options=options
        )
        if path:
            self.video_path = path
            print(f"[INFO] 选择的视频路径：{self.video_path}")
            self.cap = cv2.VideoCapture(self.video_path)
            self.is_paused = False
            self.pause_play_btn.setText('暂停')
            self.frame_count = 0

            self.timer.start(30)  # 每30ms更新一帧

    #close
    def close_all(self):
        self.close()


    def update_video_frame(self):
        if self.cap and self.cap.isOpened() and not self.is_paused:
            ret, frame = self.cap.read()
            if ret:
                current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
                print(current_frame, '/', total_frames)
                if current_frame == 1.0:
                    self.timer.stop()
                if current_frame == total_frames:
                    # 调用函数，生成视频
                    change_time = datetime.now()
                    self.generate_video_from_images_with_mmcv_and_cv2('val_segmaps', frame_rate=3)
                    insert_list = [str(self.account), self.video_path, self.output_video_path, change_time,
                                   self.algorithm_combo.currentText()]
                    self.dbcon.insert_facedata_table(insert_list)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_image)
                # 按固定大小缩放
                pixmap = pixmap.scaled(500, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                self.video_display.setPixmap(pixmap)

                if self.frame_count % int(self.interval_input.text()) == 0:
                    algorithm = self.algorithm_combo.currentText()
                    try:
                        opacity = float(self.opacity_input.text())
                        if opacity < 0 or opacity > 1:
                            raise ValueError
                    except ValueError:
                        QMessageBox.warning(self, "警告", "请输入有效的不透明度值 (0-1)", QMessageBox.Ok)
                        return

                    if self.inference_thread and self.inference_thread.isRunning():
                        self.inference_thread.terminate()
                        self.inference_thread.wait()

                    self.inference_thread = InferenceThread(frame, algorithm, opacity, model1, target_class,
                                                            background_class, current_frame)
                    self.inference_thread.result_ready.connect(self.update_result_display)
                    self.inference_thread.start()

                self.frame_count += 1
            else:
                self.timer.stop()

    def update_result_display(self, seg_pixmap):
        if not seg_pixmap.isNull():
            # 保持宽高比缩放
            seg_pixmap = seg_pixmap.scaled(
                self.result_display.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.result_display.setPixmap(seg_pixmap)

    def evaluate_video(self):

        if not self.video_path:
            QMessageBox.warning(self, "警告", "请先选择视频", QMessageBox.Ok)
            return
        self.timer.start(30)  # 每30ms更新一帧
        clear_folder('val_segmaps')

        try:
            opacity = float(self.opacity_input.text())
            if opacity < 0 or opacity > 1:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "警告", "请输入有效的不透明度值 (0-1)", QMessageBox.Ok)
            return

    def pause_play_video(self):
        if self.cap and self.cap.isOpened():
            if self.is_paused:
                self.is_paused = False
                self.pause_play_btn.setText('暂停')
                self.timer.start(30)
            else:
                self.is_paused = True
                self.pause_play_btn.setText('播放')
                self.timer.stop()

    def forward_video(self):
        if self.cap and self.cap.isOpened():
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            new_frame = current_frame + self.frames_to_skip
            if new_frame < total_frames:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
                self.frame_count = int(new_frame)
                if self.inference_thread and self.inference_thread.isRunning():
                    self.inference_thread.terminate()
                    self.inference_thread.wait()
                if not self.is_paused:
                    self.timer.start(30)

    def backward_video(self):
        if self.cap and self.cap.isOpened():
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            new_frame = current_frame - self.frames_to_skip
            if new_frame >= 0:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
                self.frame_count = int(new_frame)
                if self.inference_thread and self.inference_thread.isRunning():
                    self.inference_thread.terminate()
                    self.inference_thread.wait()
                if not self.is_paused:
                    self.timer.start(30)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SemanticSegmentation_Vedio_App("test_account")
    window.show()
    sys.exit(app.exec_())