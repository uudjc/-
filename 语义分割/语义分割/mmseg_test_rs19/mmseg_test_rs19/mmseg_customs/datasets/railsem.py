from mmseg.registry import DATASETS
from mmseg.datasets import CityscapesDataset


@DATASETS.register_module()
class RailSemDataset(CityscapesDataset):
    """RailSemDataset dataset."""
    METAINFO = dict(
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

    def __init__(self,
                 img_suffix='.png',
                 seg_map_suffix='.png',
                 **kwargs) -> None:
        super().__init__(
            img_suffix=img_suffix, seg_map_suffix=seg_map_suffix, **kwargs)
