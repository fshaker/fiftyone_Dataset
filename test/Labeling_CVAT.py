import fiftyone as fo
# from fiftyone import types

name = "SegmentAnnotate"
dataset = fo.load_dataset(name)
task_size = 4  # 21 images per task
segment_size = 4 # 4 images per job
# annotate_view = dataset.load_saved_view("SegmentAI_view")
# Sub_view = annotate_view[0:4]
Sub_view = dataset[0:4]
i=0
# for sample in dataset:
#     print(sample["ground_truth"]["detections"])
#     i+=1
#     if i>5:
#         break
anno_key = "test16"
Sub_view.annotate(
    anno_key,
    label_field = "ground_truth",
    classes=["ca", "0", "1"],
    label_type = "detections",
    task_size=task_size,
    segment_size=segment_size,
    project_name="Dataset_21_01_2-24",
    backend="cvat",
    username='shaker',
    password='XT3NraGKL3LM3XK',
    launch_editor=True,
)
#

# anno_key = "test12"
# print(dataset.load_annotation_results(anno_key))



# dataset.load_annotations(anno_key, cleanup=True)