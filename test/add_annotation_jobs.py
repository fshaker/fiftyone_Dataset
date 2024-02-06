import fiftyone as fo
# from fiftyone import types

name = "SegmentAnnotate"
dataset = fo.load_dataset(name)

annotate_view = dataset.load_saved_view("SegmentAI_view")
anno_key = "Data_21_01_2024"
annotate_view.annotate(anno_key,
                       label_field = "ground_truth",
                       backend="cvat",
                       username='shaker',
                       password='XT3NraGKL3LM3XK'
)

