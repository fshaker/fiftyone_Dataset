import fiftyone as fo


dataset_name="SegmentAnnotate"
predictions_name="mass_detections_224_conf07"

dataset = fo.load_dataset(dataset_name)
for sample in dataset:
    del sample[predictions_name]
    sample.save()
