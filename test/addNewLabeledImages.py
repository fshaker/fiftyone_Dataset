import fiftyone as fo
import os
import json
import numpy as np
import cv2


images_folder = "fiftyone_dataset/images"
annotations_folder = "fiftyone_dataset/annotations"
# dataset_name = input("What is the dataset name? ")
dataset_name = "SegmentAnnotate"
dataset = fo.load_dataset(dataset_name)
samples = []
patients = os.listdir(images_folder)
for patient in patients:
    images = os.listdir(os.path.join(images_folder, patient))
    for image in images:
        sample = {}
        image_path = os.path.join(images_folder, patient, image)
        print(image_path)
        laterality = image.split('_')[-2]
        print(laterality)
        sample["filepath"] = image_path
        metadata = fo.ImageMetadata.build_for(image_path)
        sample['metadata'] = metadata
        W = metadata["width"]
        H = metadata["height"]
        annotations_path = os.path.join(annotations_folder, patient, image.split('.')[0]+'.json')
        if os.path.exists(annotations_path):
            detections = []
            with open(annotations_path, 'r') as file:
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
                    mask = np.zeros((round(y2-y1)+2, round(x2-x1)+2), np.uint8)
                    ploygon = np.array(polyline) - [x1-1,y1-1]
                    cv2.drawContours(mask, polygon,-1,(255),1)
                    cv2.floodFill(mask, (y1//2, x1//2))

                    # polygon = (np.array(polyline) - [x1, y1]) / ((x2 - x1), (y2 - y1))
                    # print(polygon)
                    bounding_box = [float(x1) / W, float(y1) / H, float(x2 - x1) / W,
                                    float(y2 - y1) / H]
                    detections.append(fo.Detection(label=label,
                                                   bounding_box=bounding_box, mask=mask))
            sample["ground_truth"] = fo.Detections(detections=detections)

        sample["tags"] = laterality
        samples.append(sample)
    dataset.add_samples(samples)