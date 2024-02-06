import fiftyone as fo


name = "SegmentAnnotate"
dataset = fo.load_dataset(name)

session = fo.launch_app(dataset)
session.wait()
