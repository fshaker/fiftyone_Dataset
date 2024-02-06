"""
This script is used to add new data with labelme style annotations. each annotation is saved in the same folder as image

"""
import fiftyone as fo
import os
import glob
import cv2
import json
import numpy as np

tag = "SegmentAI"
def add_image_predictions(sample, annotations_file_path):
    detections = []
    img_width = sample["metadata"]["width"]
    img_height = sample["metadata"]["height"]
    with open(annotations_file_path, 'r') as file:
        annotations = json.load(file)
        for shape in annotations["shapes"]:
            label = shape['label']
            polyline = np.array(shape['points'])
            if len(polyline.shape) < 2:
                continue
            x1, y1, x2, y2 = [np.min(polyline[:, 0]), np.min(polyline[:, 1]),
                              np.max(polyline[:, 0]), np.max(polyline[:, 1])]
            # create the mask. for cv2, floodfill function,
            # the mask should be 2 pixel wider and 2 pixel taller that the contour
            mask = np.zeros([round(y2 - y1) + 2, round(x2 - x1) + 2], np.uint8)
            polygon = np.array((polyline - [x1 - 1, y1 - 1]),
                               dtype=np.int32)  # numpy.array([[1,1],[10,50],[50,50]], dtype=numpy.int32)

            print((int((y2 - y1) // 2), int((x2 - x1) // 2)))
            cv2.drawContours(mask, [polygon], -1, (255), 1)
            mask = mask > 0
            bounding_box = [float(x1) / img_width, float(y1) / img_height, float(x2 - x1) / img_width,
                            float(y2 - y1) / img_height]
            detections.append(fo.Detection(label=label, bounding_box=bounding_box, mask=mask))
        sample["ground_truth"] = fo.Detections(detections=detections)
    return sample


name = "SegmentAnnotate"
dataset = fo.load_dataset(name)
new_data_folder = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets\Segment_AI_dataset\Data_21_01_2024"

patients = os.listdir(new_data_folder)
samples = []
for patient in patients:
    images = glob.glob(os.path.join(new_data_folder, patient, "*.png"))
    print(images)
    for image_path in images:
        image_pixels = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # W, H = image_pixels.shape
        sample = fo.Sample(filepath=image_path)
        sample.compute_metadata()
        predictions_file = sample["filepath"].split('.')[0] + '.json'
        if os.path.exists(predictions_file):
            sample = add_image_predictions(sample, predictions_file)
        else:
            print("No prediction was found for image: ", image_path)
            print("predictions file: ", predictions_file)
        samples.append(sample)
        sample["tags"] = tag
dataset.add_samples(samples)