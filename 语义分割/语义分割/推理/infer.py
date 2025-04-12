# from mmseg.apis import init_model, inference_model, show_result_pyplot
# from mmengine import scandir
# import os
# from tqdm import tqdm
# import mmcv
# from mmseg.visualization import SegLocalVisualizer
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# config_path = "../mmseg_test_rs19/mmseg_test_rs19/configs/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024.py"
# checkpoint_path = "../mmseg_test_rs19/mmseg_test_rs19/ckpts/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024-6660edec.pth"
# data_root = "testdata/"
#
# output_dir = 'demo/output_frames'
# os.makedirs(output_dir, exist_ok=True)
#
# model = init_model(config_path, checkpoint_path)
#
# img_paths = scandir(data_root, suffix=".png", recursive=True)
# #
# # for img_path in tqdm(img_paths):
# #    real_path = os.path.join(data_root, img_path)
# #    # print(real_path)
# #    filename = os.path.basename(img_path)
# #    # print(filename)
# #    result = inference_model(model, real_path)
# #    # print(result)
# #    vis_image = show_result_pyplot(model, real_path, result, opacity=1, out_file=f"val_segmaps/{filename}", show=False)
# #    import matplotlib.pyplot as plt
# #
# #    # 假设 vis_image 是 numpy 数组
# #    plt.imshow(vis_image)
# #    plt.axis('off')  # 去掉坐标轴
# #    plt.show()
#
# video = mmcv.VideoReader('out.mp4')
#
#
#
#
# for i,frame in enumerate(video):
#     result = inference_model(model, frame)
#
#     seg_local_visualizer = SegLocalVisualizer(
#         vis_backends=[dict(type='LocalVisBackend')],
#         alpha=1.0)
#     seg_local_visualizer.dataset_meta = dict(
#         classes=('road', 'sidewalk', 'construction', 'tram-track', 'fence',
#                 'pole', 'traffic-light', 'traffic-sign',
#                 'vegetation', 'terrain', 'sky', 'human', 'rail-trackd',
#                 'car', 'truck', 'trackbed', 'on-rails', 'rail-raised',
#                 'rail-embeddedd'),
#         palette=[[128, 64, 128], [244, 35, 232], [70, 70, 70],
#                 [192, 0, 128], [190, 153, 153], [153, 153, 153],
#                 [250, 170, 30], [220, 220, 0], [107, 142, 35],
#                 [152, 251, 152], [70, 130, 180], [220, 20, 60],
#                 [230, 150, 140], [0, 0, 142], [0, 0, 70],
#                 [90, 40, 40], [0, 80, 100], [0, 254, 254],
#                 [0, 68, 63]])
#
#     vis_image = seg_local_visualizer.add_datasample(f'frame_{i:04d}.png', frame, result, show=False, out_file=f'{output_dir}/frame_{i:04d}.png')
#
#
#
#
# # import mmcv
# # import os
# #
# # # 创建保存图像的目录
# # save_dir = 'testdata/'
# # os.makedirs(save_dir, exist_ok=True)
# #
# # # 读取视频文件
# # video = mmcv.VideoReader('out.mp4')
# #
# # # 获取视频的前60帧
# # for i in range(min(60, len(video))):
# #     # 获取当前帧
# #     frame = video[i]
# #
# #     # 保存帧为PNG格式
# #     frame_filename = os.path.join(save_dir, f'frame_{i + 1:03d}.png')
# #     mmcv.imwrite(frame, frame_filename)
# #
# # print("前60帧已保存到 'testdata/' 目录")


import mmcv
import cv2
import os

def generate_video_from_images_with_mmcv_and_cv2(image_folder, output_video_path, frame_rate=30):
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
    video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))

    # 将每张图片添加到视频中
    for image_name in images:
        image_path = os.path.join(image_folder, image_name)
        image = mmcv.imread(image_path)
        video_writer.write(image)

    # 释放 VideoWriter 对象
    video_writer.release()
    print(f"视频已保存到 {output_video_path}")

# 调用函数，生成视频
generate_video_from_images_with_mmcv_and_cv2('val_segmaps', 'output_video.mp4', frame_rate=3)
