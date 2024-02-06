import fiftyone as fo

dataset_name = "SegmentAnnotate"
dataset = fo.load_dataset(dataset_name)

dataset.export(export_dir= r"D:\SegmentAnnotate_FoDataset",
               dataset_type = fo.types.COCODetectionDataset,
               )