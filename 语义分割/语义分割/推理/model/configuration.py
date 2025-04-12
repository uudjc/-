#-*- coding:utf-8 -*-
import os

# 程序工作路径
WORKING_PATH = os.path.abspath(os.path.dirname(__file__))

# 依赖文件存放路径
SOURCE = os.path.join(WORKING_PATH, 'dlib_model')

# 人脸的68个特征点模型文件
PREDICTOR_PATH = os.path.join(SOURCE, 'shape_predictor_68_face_landmarks.dat')

# 人脸特征描述模型文件
FACE_REC_MODEL_PATH = os.path.join(SOURCE, 'dlib_face_recognition_resnet_model_v1.dat')

#数据库路径
DATABASE_PATH = './database/database.db'

# 真实人脸与已经录入的人脸数据的相似程度的阀值，大于60认为同一人，越大就越相似
SIMILARITY_THRESHOLD = 60.0

#识别成功后，考勤打开的时间(5000 = 5s)

LED_OPEN_TIME = 5000