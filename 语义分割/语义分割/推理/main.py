import shutil
import sys
from datetime import datetime
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.QtGui import QPainter, QImage, QPixmap, QIcon
import cv2
import torch
from PyQt5.QtCore import Qt, QThread, pyqtSignal
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


class EvaluationThread(QThread):
    evaluation_finished = pyqtSignal(int, np.ndarray)
    all_finished = pyqtSignal()  # 新增信号

    def __init__(self, image_paths, algorithm, opacity):
        super().__init__()
        self.image_paths = image_paths
        self.algorithm = algorithm
        self.opacity = opacity

    def run(self):
        for index, image_path in enumerate(self.image_paths):
            try:
                result = inference_model(model1, image_path)
                if self.algorithm == '全种类分割':
                    seg_mask = show_result_pyplot(model1, image_path, result, withLabels = False, opacity=self.opacity,
                                                  out_file=f"val_segmaps/temp{index}.png",
                                                  show=False)

                elif self.algorithm == '铁道分割':
                    seg_pred = result.pred_sem_seg.data.cpu().numpy().squeeze()

                    seg_pred[seg_pred != target_class] = background_class

                    result.pred_sem_seg.data = seg_pred
                    seg_mask = show_result_pyplot(model1, image_path, result, withLabels = False,opacity=self.opacity,
                                                  out_file=f"val_segmaps/temp{index}.png",
                                                  show=False)


            except Exception as e:
                print(f"[ERROR] 图像处理失败：{str(e)}")
                continue

            # 选择模型
            print(f"[INFO] 使用{self.algorithm}进行评估...")

            print("[INFO] 发出评估完成信号")
            self.evaluation_finished.emit(index, seg_mask)


class SemanticSegmentation_Img_App(QMainWindow):
    def __init__(self, account, parent=None):
        super().__init__(parent)
        self.account = account
        self.initUI()
        self.image_paths = []
        self.evaluation_thread = None
        self.evaluation_dialog = None
        self.seg_mask_labels = []
        print(self.account)
        self.dbcon = ConnectSqlite(model.configuration.DATABASE_PATH)

    def initUI(self):
        # 主窗口设置
        self.setWindowTitle('图像质量评估系统')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #2c2c2c; color: white;")

        # 中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # 图像显示区域
        self.image_grid = QGridLayout()
        self.image_grid.setSpacing(10)
        layout.addLayout(self.image_grid)

        # 操作按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        # 选择图像按钮
        self.select_btn = QPushButton(QIcon('folder.png'), '选择图像')
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
        self.select_btn.clicked.connect(self.select_image)
        button_layout.addWidget(self.select_btn)

        # 算法选择下拉框
        self.algorithm_combo = QComboBox()
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

        self.evaluate_btn.clicked.connect(self.evaluate_image)
        button_layout.addWidget(self.evaluate_btn)

        layout.addLayout(button_layout)

    def select_image(self):
        # 打开文件选择对话框，支持多选
        options = QFileDialog.Options()
        paths, _ = QFileDialog.getOpenFileNames(
            self, "选择图像", "", "Image Files (*.png *.jpg *.jpeg)", options=options
        )
        if paths:
            self.image_paths = paths[:8]  # 最多选择 8 张图片
            print(f"[INFO] 选择的图像路径：{self.image_paths}")
            self.display_images()

    def display_images(self):
        # 清空之前的图像和分割结果标签
        for i in reversed(range(self.image_grid.count())):
            widget = self.image_grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.seg_mask_labels = []

        # 显示图像到界面
        num_cols = 4  # 每行显示 4 张图片
        for i, path in enumerate(self.image_paths):
            img = Image.open(path).convert('L')
            img = img.resize((200, 200))
            qimage = QImage(img.tobytes(), img.width, img.height, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qimage)

            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setStyleSheet("border: 2px solid #444; border-radius: 10px;")
            row = i // num_cols
            col = i % num_cols
            self.image_grid.addWidget(image_label, row * 2, col)

            seg_mask_label = QLabel()
            seg_mask_label.setStyleSheet("border: 2px solid #444; border-radius: 10px;")
            self.image_grid.addWidget(seg_mask_label, row * 2 + 1, col)
            self.seg_mask_labels.append(seg_mask_label)

    def on_algorithm_selected(self, index):
        algorithm = self.algorithm_combo.currentText()
        print(f"[INFO] 选择的算法：{algorithm}")

    def evaluate_image(self):
        if not self.image_paths:
            QMessageBox.warning(self, "警告", "请先选择图像", QMessageBox.Ok)
            return

        algorithm = self.algorithm_combo.currentText()
        try:
            opacity = float(self.opacity_input.text())
            if opacity < 0 or opacity > 1:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "警告", "请输入有效的不透明度值 (0-1)", QMessageBox.Ok)
            return

        self.evaluation_thread = EvaluationThread(self.image_paths, algorithm, opacity)
        self.evaluation_thread.evaluation_finished.connect(self.on_evaluation_finished)
        self.evaluation_dialog = QMessageBox(self)
        self.evaluation_dialog.setWindowTitle("提示")
        self.evaluation_dialog.setText("正在评估，请稍后...")
        self.evaluation_dialog.setStandardButtons(QMessageBox.NoButton)
        print("[INFO] 显示评估提示框")
        self.evaluation_dialog.show()
        self.evaluation_thread.start()

    def close_all(self):
        self.close()

    def on_evaluation_finished(self, index, seg_mask):
        print("[INFO] 收到评估完成信号")
        if self.evaluation_dialog:
            print("[INFO] 尝试关闭评估提示框")
            try:
                # 尝试使用 hide 方法
                self.evaluation_dialog.hide()
                self.evaluation_dialog.deleteLater()
                print("[INFO] 评估提示框已关闭")
            except Exception as e:
                print(f"[ERROR] 关闭评估提示框时出错：{e}")
        if index < len(self.seg_mask_labels):
            # 加载保存的分割结果图片
            image_path = f"val_segmaps/temp{index}.png"
            current_time = datetime.now().strftime('%Y%m%d%H%M%S')
            output_video_path = f'pic/{current_time}_{index}.png'
            # 复制文件
            shutil.copy(image_path, output_video_path)
            print(f"图片已复制到 {output_video_path}")

            pixmap = QPixmap(image_path)

            if not pixmap.isNull():
                # 获取 seg_mask_label 的大小
                label_size = self.seg_mask_labels[index].size()
                # 对 pixmap 进行缩放
                scaled_pixmap = pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.seg_mask_labels[index].setPixmap(scaled_pixmap)
            else:
                print(f"[ERROR] 无法加载图片: {image_path}")

            try:
                face_img_path = self.image_paths[index]

                change_time = datetime.now()
                # 修改插入数据类型  "用户", "方式", "路径", "时间", "分割结果"
                insert_list = [str(self.account), face_img_path, output_video_path, change_time, self.algorithm_combo.currentText()]
                self.dbcon.insert_facedata_table(insert_list)
            except Exception as e:
                print(f"插入数据 函数出现异常: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SemanticSegmentation_Img_App("test_account")
    window.show()
    sys.exit(app.exec_())
