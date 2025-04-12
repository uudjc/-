# Copyright (c) OpenMMLab. All rights reserved.
import argparse
import os
import os.path as osp
import time

import numpy as np
import torch
from mmengine import Config
from mmengine.fileio import dump
from mmengine.model.utils import revert_sync_batchnorm
from mmengine.registry import init_default_scope
from mmengine.runner import Runner, load_checkpoint
from mmengine.utils import mkdir_or_exist
from mmengine.config import DictAction

from mmseg.registry import MODELS


def parse_args():
    parser = argparse.ArgumentParser(description='MMSeg benchmark a model')
    parser.add_argument('config', help='test config file path')
    parser.add_argument('checkpoint', help='checkpoint file')
    parser.add_argument(
        '--log-interval', type=int, default=50, help='interval of logging')
    parser.add_argument(
        '--work-dir',
        help=('if specified, the results will be dumped '
              'into the directory as json'))
    parser.add_argument('--repeat-times', type=int, default=1)
    parser.add_argument('--data-root', type=str, default='data/railsem19/')
    parser.add_argument('--image-prefix', type=str, default='image/test')
    parser.add_argument('--label-prefix', type=str, default='label/test')
    parser.add_argument(
        '--launcher',
        choices=['none', 'pytorch', 'slurm', 'mpi'],
        default='none',
        help='job launcher')
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
             'in xxx=yyy format will be merged into config file. If the value to '
             'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
             'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
             'Note that the quotation marks are necessary and that no white space '
             'is allowed.')
    # When using PyTorch version >= 2.0.0, the `torch.distributed.launch`
    # will pass the `--local-rank` parameter to `tools/train.py` instead
    # of `--local_rank`.
    parser.add_argument('--local_rank', '--local-rank', type=int, default=0)
    args = parser.parse_args()
    if 'LOCAL_RANK' not in os.environ:
        os.environ['LOCAL_RANK'] = str(args.local_rank)
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    cfg = Config.fromfile(args.config)
    cfg.launcher = args.launcher
    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)

    init_default_scope(cfg.get('default_scope', 'mmseg'))

    timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime())
    if args.work_dir is not None:
        mkdir_or_exist(osp.abspath(args.work_dir))
        json_file = osp.join(args.work_dir, f'fps_{timestamp}.json')
    else:
        # use config filename as default work_dir if cfg.work_dir is None
        work_dir = osp.join('./work_dirs',
                            osp.splitext(osp.basename(args.config))[0])
        mkdir_or_exist(osp.abspath(work_dir))
        json_file = osp.join(work_dir, f'fps_{timestamp}.json')

    repeat_times = args.repeat_times
    # set cudnn_benchmark
    torch.backends.cudnn.benchmark = False
    cfg.model.pretrained = None

    benchmark_dict = dict(config=args.config, unit='img / s')
    overall_fps_list = []
    cfg.test_dataloader.batch_size = 1  # ensures test batch_size = 1

    cfg.test_dataloader.dataset.data_prefix.img_path = args.image_prefix
    cfg.test_dataloader.dataset.data_prefix.seg_map_path = args.label_prefix
    cfg.test_dataloader.dataset.data_root = args.data_root

    # build the runner
    runner = Runner.from_cfg(cfg)
    for time_index in range(repeat_times):
        print(f'Run {time_index + 1}:')

        # build the dataloader
        data_loader = runner.test_dataloader

        # build the model and load checkpoint
        cfg.model.train_cfg = None
        model = MODELS.build(cfg.model)

        if 'checkpoint' in args and osp.exists(args.checkpoint):
            load_checkpoint(model, args.checkpoint, map_location='cpu')

        if torch.cuda.is_available():
            model = model.cuda()

        model = revert_sync_batchnorm(model)

        # build the evaluator
        evaluator = runner.test_evaluator

        # the first several iterations may be very slow so skip them
        num_warmup = 0
        pure_inf_time = 0
        total_iters = len(data_loader.dataset)

        runner.call_hook('before_run')
        runner.call_hook('before_test')
        runner.call_hook('before_test_epoch')

        model.eval()

        # benchmark with total_iters batches and take the average
        for i, data_batch in enumerate(data_loader):
            data = model.data_preprocessor(data_batch, True)
            inputs = data['inputs']
            data_samples = data['data_samples']
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            start_time = time.perf_counter()

            with torch.no_grad():
                outputs = model(inputs, data_samples, mode='predict')

            if torch.cuda.is_available():
                torch.cuda.synchronize()
            elapsed = time.perf_counter() - start_time

            evaluator.process(data_samples=outputs, data_batch=data_batch)

            if i >= num_warmup:
                pure_inf_time += elapsed
                if (i + 1) % args.log_interval == 0:
                    fps = (i + 1 - num_warmup) / pure_inf_time
                    print(f'Done image [{i + 1:<3}/ {total_iters}], '
                          f'fps: {fps:.2f} img / s')

            if (i + 1) == total_iters:
                fps = (i + 1 - num_warmup) / pure_inf_time
                print(f'Overall fps: {fps:.2f} img / s\n')
                benchmark_dict[f'overall_fps_{time_index + 1}'] = round(fps, 2)
                overall_fps_list.append(fps)
                break

        # calculate the metrics
        metrics = evaluator.evaluate(len(data_loader.dataset))
        # print the testing results
        runner.call_hook('after_test_epoch', metrics=metrics)
        runner.call_hook('after_test')
        runner.call_hook('after_run')
        print(f'Pure inf time: {pure_inf_time:.2f} s')
        fps = total_iters / pure_inf_time
        print(f'Overall fps: {fps:.2f} img / s\n')

    benchmark_dict['average_fps'] = round(np.mean(overall_fps_list), 2)
    benchmark_dict['fps_variance'] = round(np.var(overall_fps_list), 4)

    print(f'Average fps of {repeat_times} evaluations: '
          f'{benchmark_dict["average_fps"]}')
    print(f'The variance of {repeat_times} evaluations: '
          f'{benchmark_dict["fps_variance"]}')
    dump(benchmark_dict, json_file, indent=4)


if __name__ == '__main__':
    main()
