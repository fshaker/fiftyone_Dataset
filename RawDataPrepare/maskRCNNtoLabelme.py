"""
This script is used after inference_30000it on unlabeled dataset to make the dataset ready for LabelMe annotation.
"""
import os
from skimage.io import imread
import json
from imantics import Mask

# The AI model that is used, finds five classes as numbers: (1, 2, 3, 4, 5). These numbers are indicators of
# string labels: ("ca", "mass", "ln", "ca16", "ad"). Our code will change the number labels into their corresponding string labels.
labels = {"1":"ca",
          "2":"mass",
          "3": "ln",
          "4": "ca16",
          "5": "ad"}
flags = {
            "__ignore__": True,
            "Entirely Fatty": False,
            "Fibroglandular Density": False,
            "Heterogeneously Dense": False,
            "Extremely Dense": False,
            "BI-RADS 0": False,
            "BI-RADS 1": False,
            "BI-RADS 2": True,
            "BI-RADS 3": False,
            "BI-RADS 4": False,
            "BI-RADS 4 A": False,
            "BI-RADS 4 B": False,
            "BI-RADS 4 C": False,
            "BI-RADS 5": False,
            "BI-RADS 6": False,
            "Axillary Lymph Nodes": False
        }
# annotations_dir = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets\Segment_AI_dataset\inference_output"
dest_dir = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets\Segment_AI_dataset\images"
annotations_dir = "../results/tmp/output/RUN_11_configs/inference_output"
patients = os.listdir(annotations_dir)

for patient in patients:
    annotations = os.listdir(os.path.join(annotations_dir, patient))
    for annotation in annotations:
        with open(os.path.join(annotations_dir, patient, annotation), 'r') as json_file:
            annotation_content = json.load(json_file)
        labelme_annot = {}
        labelme_annot["version"] = "5.3.1"
        labelme_annot["flags"] = flags

        shapes = annotation_content["shapes"]

        labelme_shapes = []
        for shap in shapes:
            if shap["label"] == "2" or shap["label"] == "5" or shap["label"] == "3": # shap["label"] == "2" or
                print(shap["label"])
                continue
            l_shape = {}
            mask = shap["mask"]
            bbox = shap["bbox"]
            im_mask = Mask(mask)
            polygons = im_mask.polygons().points
            for polygon in polygons:
                polygon = polygon+bbox[:2]
                l_shape["points"] = polygon.tolist()
                print(polygon.tolist())
                l_shape["label"] = labels[shap["label"]]
                l_shape["group_id"] = None
                l_shape["description"] = ""
                l_shape["shape_type"] = "polygon"
                l_shape["flags"] = {}
                labelme_shapes.append(l_shape)
        labelme_annot["shapes"] = labelme_shapes
        labelme_annot["imagePath"] = os.path.basename(annotation_content["imagePath"])
        labelme_annot["imageData"] = None
        image = imread(annotation_content["imagePath"], as_gray=True)
        H, W = image.shape
        labelme_annot["imageHeight"] = H
        labelme_annot["imageWidth"] = W
        labelme_annotation_file_path = os.path.join(dest_dir,patient,annotation)
        with open(labelme_annotation_file_path, 'w') as dest_file:
            json.dump(labelme_annot, dest_file, sort_keys=False, indent=4)


