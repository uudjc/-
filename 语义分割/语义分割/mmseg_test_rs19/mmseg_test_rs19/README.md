# 一、环境配置

本模型运行环境要求Python 3.7+，CUDA 10.2+，PyTorch 1.8+。推荐使用Python 3.8，CUDA 11.1，PyTorch 1.9.0进行复现。

使用如下命令新建并激活环境：

```shell
conda create -n rs19 python=3.8 -y
conda activate rs19
```

我们提供了两种环境配置方式，任选其一均可：

## 1. 手动配置（推荐）

可以按照如下步骤手动安装，

1. 安装PyTorch

    按照PyTorch官网的要求，参照CUDA环境安装PyTorch：

    ```shell
    pip install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
    ```
pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
2. 安装MMSegmentation框架：

    ```shell
    pip install -U openmim
    mim install mmengine
    mim install "mmcv==2.0.1"
    pip install "mmsegmentation==1.1.2"
    ```

## 2. 从requirements.txt安装

可以使用目录下提供的requirements.txt直接安装。

```shell
pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.9/index.html
pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html -f https://download.openmmlab.com/mmcv/dist/cu101/torch1.7/index.html
```

# 二、数据集准备

在项目根目录下准备data文件夹，并将数据集文件夹置于data下。

## 1. 数据集结构

数据集应当具有如下结构，其中 `data/railsem19/image/test/` 下存放测试集图片， `data/railsem19/label/test/` 下存放测试集标签：

```shell
data
├── railsem19
│   ├── image
│   │   ├── train
│   │   ├── val
│   │   ├── test
│   │   └── ...
│   ├── label
│   │   ├── train
│   │   ├── val
│   │   ├── test
│   │   └── ...
│   └── ...
└── ...
```

注：若数据集不位于data文件夹下，也可以在测试脚本中使用参数 `--data-root` 指定位置

# 三、开始测试

## 1.参数说明

脚本提供如下可选参数，其含义与默认值如下表所示

| 参数名称           | 参数含义   | 默认值              |
|----------------|--------|------------------|
| `--repeat-times` | 完整测试次数 | 1                |
| `--data-root`    | 测试集根路径  | "data/railsem19" |
| `--image-prefix` | 图片相对路径 | "image/test"     |
| `--label-prefix` | 标签相对路径 | "label/test"     |

关于 `--repeat-times` ，由于模型在运行初期较慢，测试运行时间会有抖动，因此我们建议运行多次（例如3次），取平均值作为最终结果。

如采用默认值，图片最终会从 `data/railsem19/image/test/` 中进行查找，标签最终会从 `data/railsem19/label/test/` 中进行查找。

## 2.测试脚本示例

测试脚本范例如下，在项目根目录下执行：

```shell
python -m test --data-root=data/railsem19 --image-prefix=image/test --label-prefix=label/test --repeat-times=3 configs/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024.py ckpts/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024-6660edec.pth
```

其中 `configs/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024.py` 是配置文件路径， `ckpts/ddrnet_23-slim_1xb2-120k_city2railsem-1024x1024-6660edec.pth` 是模型文件路径。

如果数据集路径不在默认位置，则需修改 `--data-root` 参数；如果数据集结构和默认不一致，则需修改 `--image-prefix` 和 `--label-prefix` 参数。

## 3.测试结果说明

测试结果算法精度指标（mIoU）、模型推理时间（秒）、以及模型推理速度（FPS）。

测试输出中：

+ `mmengine - INFO - Iter(test)` 输出后跟随的 `mIoU` 一项提供了算法精度指标（mIoU）
+ `Pure inf time` 输出提供了模型推理时间（s）
+ `Overall fps` 输出提供了模型在测试数据集上的推理速度（FPS）

如果进行多轮测试，多轮测试中的mIoU指标一致，且多轮测试中FPS的平均值由 `Average fps of 3 evaluations` 输出提供。

# 备注：训练方案

我们采用ddrnet_23-slim网络结构，在4张NVIDIA GeForce RTX 3090上，batch_size=2的设定下进行了120k次迭代训练。

我们采用ddrnet_23-slim在Cityscapes数据集上的预训练模型进行初始化，进而在提供的RailSem19数据集上进行正式训练。
