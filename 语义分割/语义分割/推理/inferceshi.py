from mmseg.apis import init_model, inference_model, show_result_pyplot
from mmengine import scandir
import os
from tqdm import tqdm
import mmcv
from mmseg.visualization import SegLocalVisualizer



config_path = "../mmseg_test_rs19/mmseg_test_rs19/configs/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024.py"
checkpoint_path = "../mmseg_test_rs19/mmseg_test_rs19/ckpts/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024-6660edec.pth"
data_root = "testdata/"

output_dir = 'demo/output_frames'
os.makedirs(output_dir, exist_ok=True)

model = init_model(config_path, checkpoint_path)
target_class = 17
background_class = 0

img_paths = scandir(data_root, suffix=".png", recursive=True)

for img_path in tqdm(img_paths):
   real_path = os.path.join(data_root, img_path)
   filename = os.path.basename(img_path)
   result = inference_model(model, real_path)
   seg_pred = result.pred_sem_seg.data.cpu().numpy().squeeze()

   seg_pred[seg_pred != target_class] = background_class

   result.pred_sem_seg.data = seg_pred
   vis_image = show_result_pyplot(model, real_path, result, opacity=1,  out_file=f"val_segmaps/{filename}", show=False)



video = mmcv.VideoReader('out.mp4')



for i,frame in enumerate(video):
    result = inference_model(model, frame)

    seg_pred = result.pred_sem_seg.data.cpu().numpy().squeeze()

    seg_pred[seg_pred != target_class] = background_class

    result.pred_sem_seg.data = seg_pred



    seg_local_visualizer = SegLocalVisualizer(
        vis_backends=[dict(type='LocalVisBackend')],
        alpha=0.5)
    seg_local_visualizer.dataset_meta = dict(
        classes=('road', 'sidewalk', 'construction', 'tram-track', 'fence',
                'pole', 'traffic-light', 'traffic-sign',
                'vegetation', 'terrain', 'sky', 'human', 'rail-trackd',
                'car', 'truck', 'trackbed', 'on-rails', 'rail-raised',
                'rail-embeddedd'),
        palette=[[128, 64, 128], [244, 35, 232], [70, 70, 70],
                [192, 0, 128], [190, 153, 153], [153, 153, 153],
                [250, 170, 30], [220, 220, 0], [107, 142, 35],
                [152, 251, 152], [70, 130, 180], [220, 20, 60],
                [230, 150, 140], [0, 0, 142], [0, 0, 70],
                [90, 40, 40], [0, 80, 100], [0, 254, 254],
                [0, 68, 63]])
    vis_image = seg_local_visualizer.add_datasample(f'frame_{i:04d}.png', frame, result, show=False, out_file=f'{output_dir}/frame_{i:04d}.png')


