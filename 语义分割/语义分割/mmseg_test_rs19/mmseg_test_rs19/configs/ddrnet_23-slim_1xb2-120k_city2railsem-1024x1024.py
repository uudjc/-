_base_ = ['./custom_imports.py']

checkpoint = 'https://download.openmmlab.com/mmsegmentation/v0.5/ddrnet/pretrain/ddrnet23s-in1kpre_3rdparty-1ccac5b1.pth'
class_weight = [
    0.9553,
    0.9705,
    0.8989,
    1.0291,
    0.98,
    0.9658,
    1.1395,
    1.1392,
    0.8716,
    0.9194,
    0.874,
    1.1359,
    0.928,
    1.0697,
    1.144,
    0.9049,
    1.0071,
    0.9734,
    1.0938,
]
crop_size = (
    1024,
    1024,
)
data_preprocessor = dict(
    bgr_to_rgb=True,
    mean=[
        123.675,
        116.28,
        103.53,
    ],
    pad_val=0,
    seg_pad_val=255,
    size=(
        1024,
        1024,
    ),
    std=[
        58.395,
        57.12,
        57.375,
    ],
    type='SegDataPreProcessor')
data_root = 'data/railsem19/'
dataset_type = 'RailSemDataset'
default_hooks = dict(
    checkpoint=dict(
        by_epoch=False,
        interval=12000,
        out_dir='./ckpts',
        save_best='mIoU',
        type='CheckpointHook'),
    logger=dict(interval=50, log_metric_by_epoch=False, type='LoggerHook'),
    param_scheduler=dict(type='ParamSchedulerHook'),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    timer=dict(type='IterTimerHook'),
    visualization=dict(type='SegVisualizationHook'))
default_scope = 'mmseg'
env_cfg = dict(
    cudnn_benchmark=True,
    dist_cfg=dict(backend='nccl'),
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0))
img_ratios = [
    0.5,
    0.75,
    1.0,
    1.25,
    1.5,
    1.75,
]
iters = 120000
launcher = 'pytorch'
load_from = 'checkpoint/ddrnet_23-slim_in1k-pre_2xb6-120k_cityscapes-1024x1024_20230426_145312-6a5e5174.pth'
log_level = 'INFO'
log_processor = dict(by_epoch=False)
model = dict(
    backbone=dict(
        align_corners=False,
        channels=32,
        in_channels=3,
        init_cfg=dict(
            checkpoint=
            'https://download.openmmlab.com/mmsegmentation/v0.5/ddrnet/pretrain/ddrnet23s-in1kpre_3rdparty-1ccac5b1.pth',
            type='Pretrained'),
        norm_cfg=dict(requires_grad=True, type='SyncBN'),
        ppm_channels=128,
        type='DDRNet'),
    data_preprocessor=dict(
        bgr_to_rgb=True,
        mean=[
            123.675,
            116.28,
            103.53,
        ],
        pad_val=0,
        seg_pad_val=255,
        size=(
            1024,
            1024,
        ),
        std=[
            58.395,
            57.12,
            57.375,
        ],
        type='SegDataPreProcessor'),
    decode_head=dict(
        align_corners=False,
        channels=64,
        dropout_ratio=0.0,
        in_channels=128,
        loss_decode=[
            dict(
                class_weight=[
                    0.9553,
                    0.9705,
                    0.8989,
                    1.0291,
                    0.98,
                    0.9658,
                    1.1395,
                    1.1392,
                    0.8716,
                    0.9194,
                    0.874,
                    1.1359,
                    0.928,
                    1.0697,
                    1.144,
                    0.9049,
                    1.0071,
                    0.9734,
                    1.0938,
                ],
                loss_weight=1.0,
                min_kept=131072,
                thres=0.9,
                type='OhemCrossEntropy'),
            dict(
                class_weight=[
                    0.9553,
                    0.9705,
                    0.8989,
                    1.0291,
                    0.98,
                    0.9658,
                    1.1395,
                    1.1392,
                    0.8716,
                    0.9194,
                    0.874,
                    1.1359,
                    0.928,
                    1.0697,
                    1.144,
                    0.9049,
                    1.0071,
                    0.9734,
                    1.0938,
                ],
                loss_weight=0.4,
                min_kept=131072,
                thres=0.9,
                type='OhemCrossEntropy'),
        ],
        norm_cfg=dict(requires_grad=True, type='SyncBN'),
        num_classes=19,
        type='DDRHead'),
    test_cfg=dict(mode='whole'),
    train_cfg=dict(),
    type='EncoderDecoder')
norm_cfg = dict(requires_grad=True, type='SyncBN')
optim_wrapper = dict(
    clip_grad=None,
    optimizer=dict(lr=0.01, momentum=0.9, type='SGD', weight_decay=0.0005),
    type='OptimWrapper')
optimizer = dict(lr=0.01, momentum=0.9, type='SGD', weight_decay=0.0005)
param_scheduler = [
    dict(
        begin=0,
        by_epoch=False,
        end=120000,
        eta_min=0,
        power=0.9,
        type='PolyLR'),
]
randomness = dict(seed=304)
resume = False
test_cfg = dict(type='TestLoop')
test_dataloader = dict(
    batch_size=1,
    dataset=dict(
        data_prefix=dict(img_path='image/val', seg_map_path='label/val'),
        data_root='data/railsem19/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(keep_ratio=True, scale=(
                1536,
                1024,
            ), type='Resize'),
            dict(type='LoadAnnotations'),
            dict(type='PackSegInputs'),
        ],
        type='RailSemDataset'),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
test_evaluator = dict(
    iou_metrics=[
        'mIoU',
    ], type='IoUMetric')
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(keep_ratio=True, scale=(
        1536,
        1024,
    ), type='Resize'),
    dict(type='LoadAnnotations'),
    dict(type='PackSegInputs'),
]
train_cfg = dict(
    max_iters=120000, type='IterBasedTrainLoop', val_interval=12000)
train_dataloader = dict(
    batch_size=2,
    dataset=dict(
        data_prefix=dict(
            img_path='image/new_train', seg_map_path='label/new_train'),
        data_root='data/railsem19/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadAnnotations'),
            dict(
                keep_ratio=True,
                ratio_range=(
                    0.5,
                    2.0,
                ),
                scale=(
                    1536,
                    1024,
                ),
                type='RandomResize'),
            dict(
                cat_max_ratio=0.75,
                crop_size=(
                    1024,
                    1024,
                ),
                type='RandomCrop'),
            dict(prob=0.5, type='RandomFlip'),
            dict(type='PhotoMetricDistortion'),
            dict(type='PackSegInputs'),
        ],
        seg_map_suffix='.png',
        type='RailSemDataset'),
    num_workers=2,
    persistent_workers=True,
    sampler=dict(shuffle=True, type='InfiniteSampler'))
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations'),
    dict(
        keep_ratio=True,
        ratio_range=(
            0.5,
            2.0,
        ),
        scale=(
            1536,
            1024,
        ),
        type='RandomResize'),
    dict(cat_max_ratio=0.75, crop_size=(
        1024,
        1024,
    ), type='RandomCrop'),
    dict(prob=0.5, type='RandomFlip'),
    dict(type='PhotoMetricDistortion'),
    dict(type='PackSegInputs'),
]
tta_model = dict(type='SegTTAModel')
tta_pipeline = [
    dict(backend_args=None, type='LoadImageFromFile'),
    dict(
        transforms=[
            [
                dict(keep_ratio=True, scale_factor=0.5, type='Resize'),
                dict(keep_ratio=True, scale_factor=0.75, type='Resize'),
                dict(keep_ratio=True, scale_factor=1.0, type='Resize'),
                dict(keep_ratio=True, scale_factor=1.25, type='Resize'),
                dict(keep_ratio=True, scale_factor=1.5, type='Resize'),
                dict(keep_ratio=True, scale_factor=1.75, type='Resize'),
            ],
            [
                dict(direction='horizontal', prob=0.0, type='RandomFlip'),
                dict(direction='horizontal', prob=1.0, type='RandomFlip'),
            ],
            [
                dict(type='LoadAnnotations'),
            ],
            [
                dict(type='PackSegInputs'),
            ],
        ],
        type='TestTimeAug'),
]
val_cfg = dict(type='ValLoop')
val_dataloader = dict(
    batch_size=1,
    dataset=dict(
        data_prefix=dict(
            img_path='image/new_val', seg_map_path='label/new_val'),
        data_root='data/railsem19/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(keep_ratio=True, scale=(
                1536,
                1024,
            ), type='Resize'),
            dict(type='LoadAnnotations'),
            dict(type='PackSegInputs'),
        ],
        seg_map_suffix='.png',
        type='RailSemDataset'),
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
val_evaluator = dict(
    iou_metrics=[
        'mIoU',
    ], type='IoUMetric')
vis_backends = [
    dict(type='LocalVisBackend'),
]
visualizer = dict(
    name='visualizer',
    type='SegLocalVisualizer',
    vis_backends=[
        dict(type='LocalVisBackend'),
    ])
work_dir = './work_dirs/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024_new_nolc_dist'
