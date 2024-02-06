import fiftyone as fo
import os
import json
import numpy as np
import cv2


# datasets = fo.list_datasets()
# for dataset in datasets:
#     data = fo.load_dataset(dataset)
#     data.delete()
name = "SegmentAnnotate"
images_dir = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets\Segment+Annotate_v1\test"
dataset = fo.Dataset.from_images_dir(images_dir, name=name, persistent=True, overwrite=True)
dataset.compute_metadata()
for sample in dataset:
    # We assume that the annotation file has the same name as the image file except for the extention.
    # This assumption is true for LabelMe annotation format
    annotations_path = sample["filepath"].split('.')[0]+'.json'
    img_width = sample["metadata"]["width"]
    img_height = sample["metadata"]["height"]
    detections = []
    with open(annotations_path, 'r') as file:
        annotations = json.load(file)
        for shape in annotations["shapes"]:
            label = shape['label']
            polyline = np.array(shape['points'])
            if len(polyline.shape)<2:
                continue
            x1, y1, x2, y2 = [np.min(polyline[:, 0]), np.min(polyline[:, 1]),
                              np.max(polyline[:, 0]), np.max(polyline[:, 1])]

            mask = np.zeros([round(y2-y1)+2, round(x2-x1)+2], np.uint8)
            polygon = np.array((polyline - [x1-1, y1-1]), dtype=np.int32) #numpy.array([[1,1],[10,50],[50,50]], dtype=numpy.int32)
            # print(mask.shape)
            # print(mask_with_contours.shape)
            print((int((y2-y1)//2), int((x2-x1)//2)))
            cv2.drawContours(mask, [polygon],-1,(255),1)
            mask = mask>0
            bounding_box = [float(x1) / img_width, float(y1) / img_height, float(x2 - x1) / img_width,
                            float(y2 - y1) / img_height]
            detections.append(fo.Detection(label=label,
                                           bounding_box=bounding_box, mask = mask))
    sample["ground_truth"] = fo.Detections(detections=detections)
    sample.save()

# for sample in dataset:
#     img_width = sample["metadata"]["width"]
#     img_height = sample["metadata"]["height"]
#     image_file = (sample["filepath"])
#     predictions_file = os.path.basename(sample["filepath"]).split('.')[0]+'.json'
#     predictions_top_folder = os.path.basename(os.path.dirname(sample["filepath"]))
#     predictions_file_path = os.path.join(predictions_dir, predictions_top_folder, predictions_file)
#     if not os.path.exists(predictions_file_path):
#         print("No Predictions", predictions_file_path)
#         sample["tags"]=["train"]
#         sample.save()
#         continue
#     predictions_folder = image_file.split(os.sep)[-2]
#     annotations_path = os.path.join(predictions_dir, predictions_folder,predictions_file)
#     detections = []
#     with open(annotations_path, 'r') as file:
#         annotations = json.load(file)
#         for shape in annotations["shapes"]:
#             label = shape['label']
#             x1, y1, x2, y2 = shape['bbox']
#             bounding_box = [float(x1) / img_width, float(y1) / img_height, float(x2 - x1) / img_width,
#                             float(y2 - y1) / img_height]
#             mask = np.array(shape['mask']) > 0
#             if len(mask.shape) < 2:
#                 mask = np.zeros((10, 10))
#             elif (mask.shape[0]) == 0 or (mask.shape[1]) == 0:
#                 mask = np.zeros((10, 10))
#             confidence = float(shape['confidence'])
#             detections.append(fo.Detection(label=label, bounding_box=bounding_box, mask=mask, confidence=confidence))
#     sample["predictions"] = fo.Detections(detections=detections)
#     sample["tags"]=["test"]
#     sample.save()


# session = fo.launch_app(dataset)