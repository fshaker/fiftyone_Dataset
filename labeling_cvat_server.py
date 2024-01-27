import sys
import fiftyone as fo


# anno_key  = sys.argv[1]
# print(anno_key)
name = "SegmentAI"
dataset = fo.load_dataset(name)
task_size = 84  # 21 images per task
segment_size = 4 # 4 images per job
Sub_view = dataset[0:4]
i=0

anno_key = f"task_{i}"
subview = dataset[0:84]

subview.annotate(
    anno_key,
    label_field = "polygons",
    classes=["ca"],
    label_type = "polygons",
    task_size=task_size,
    segment_size=segment_size,
    project_name="Dataset_22_01_2-24",
    backend="cvat",
    username='mehrasnorouzi',
    password='U9JzcBCEbsW9Nsr',
    # launch_editor=True,
)
i+=1
anno_key = f"task_{i}"
subview = dataset[84:132]
task_size = 48
subview.annotate(
    anno_key,
    label_field = "polygons",
    classes=["ca"],
    label_type = "polygons",
    task_size=task_size,
    segment_size=segment_size,
    project_name="Dataset_22_01_2-24",
    backend="cvat",
    username='m.hasanpor',
    password='A7kV5cS7imHBq67',
    # launch_editor=True,
)
i+=1
anno_key = f"task_{i}"
subview = dataset[132:134]
subview.annotate(
    anno_key,
    label_field = "polygons",
    classes=["ca"],
    label_type = "polygons",
    task_size=2,
    segment_size=2,
    project_name="Dataset_22_01_2-24",
    backend="cvat",
    username='m.hasanpor',
    password='A7kV5cS7imHBq67',
    # launch_editor=True,
)
i+=1
anno_key = f"task_{i}"
subview = dataset[134:166]
task_size = 32
subview.annotate(
    anno_key,
    label_field = "polygons",
    classes=["ca"],
    label_type = "polygons",
    task_size=task_size,
    segment_size=segment_size,
    project_name="Dataset_22_01_2-24",
    backend="cvat",
    username='m.hasanpor',
    password='A7kV5cS7imHBq67',
    # launch_editor=True,
)