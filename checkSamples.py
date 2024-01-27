import fiftyone as fo
import os
import glob


name = "SegmentAnnotate"
dataset = fo.load_dataset(name)
segmentAI_view = dataset.load_saved_view("SegmentAI_view")
new_data_folder = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets\Segment_AI_dataset\Data_21_01_2024"

patients = os.listdir(new_data_folder)
samples = segmentAI_view[0:4]
for sample in samples:
    print(sample["filepath"])
    print(sample)
    print(sample["ground_truth"]["detections"])
# for patient in patients:
#     images = glob.glob(os.path.join(new_data_folder, patient, "*.png"))
#     for image_path in images:
#         sample = dataset[filepath==image_path]
