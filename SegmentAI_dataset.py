import fiftyone as fo
import os
import json
import numpy as np


name = "SegmentAI"

images_dir = "/root/datasets/Segment_AI/Data_21_01_2024"
annotations_dir = "/root/datasets/Segment_AI/Data_21_01_2024"

dataset = fo.Dataset.from_images_dir(images_dir, name=name, persistent=True, overwrite=True)
dataset.compute_metadata()
for sample in dataset:
    image_folder_name = os.path.basename(os.path.dirname(sample["filepath"]))
    annotations_file = os.path.basename(sample["filepath"]).split('.')[0]+'.json'
    annotations_path = os.path.join(annotations_dir, image_folder_name, annotations_file)
    print(sample["metadata"])
    if sample["metadata"] is None:
        print(sample["filepath"])
        continue
    img_width = sample["metadata"]["width"]
    img_height = sample["metadata"]["height"]
    detections = []
    polylines = []
    if not os.path.exists(annotations_path):
        continue
    with open(annotations_path, 'r') as file:
        annotations = json.load(file)
        for shape in annotations["shapes"]:
            label = shape['label']
            polyline = np.array(shape['points'])
            if len(polyline.shape)<2:
                continue
            x1, y1, x2, y2 = [np.min(polyline[:, 0]), np.min(polyline[:, 1]),
                              np.max(polyline[:, 0]), np.max(polyline[:, 1])]
            if (x2==x1) or (y2==y1):
                continue
            polygon = (np.array(polyline)-[x1, y1])/((x2-x1),(y2-y1))
            # print(polygon)
            bounding_box = [float(x1) / img_width, float(y1) / img_height, float(x2 - x1) / img_width,
                            float(y2 - y1) / img_height]
            detections.append(fo.Detection(label=label,
                                           bounding_box=bounding_box, polygon =polygon))

            polygon = (np.array(polyline))/(img_width,img_height)
            polylines.append(fo.Polyline(label=label, points=[polygon], closed=True, filled=True))
    sample["ground_truth"] = fo.Detections(detections=detections)
    sample["polygons"] = fo.Polylines(polylines=polylines)
    sample.save()
