import copy
import glob
import os
import json
from tkinter import filedialog
import numpy as np
import cv2
import PIL.Image
from PIL.Image import Image, fromarray
from imantics import Mask

def merge_annotations(labelme_annos, yolo_annos):
    annotations = copy.deepcopy(labelme_annos)
    shapes = annotations['shapes']
    yolo_shapes = yolo_annos['shapes']
    if len(shapes) == 0:
        return annotations
    for shape in yolo_shapes:
        if shape['label'] == 'mass':
            l_shape = {}
            mask = shape["mask"]
            mask_img = np.array(mask, dtype=np.uint8)
            if mask_img.ndim <2: continue
            # mask_H, mask_W = mask_img.shape[:2]
            # cv2.imwrite(yolo_annos['imagePath'].split('.')[0]+'_mask.png', mask_img*255)
            H, W = yolo_annos["image_shape"]
            mask_img = cv2.resize(mask_img, (W, H), interpolation=cv2.INTER_NEAREST)
            im_mask = Mask(mask_img)
            # cv2.imwrite(yolo_annos['imagePath'].split('.')[0]+'_big_mask.png', mask_img*255)
            polygons = im_mask.polygons().points
            for polygon in polygons:
                l_shape["points"] = polygon.tolist()
                print(polygon.tolist())
                l_shape["label"] = shape['label']
                l_shape["group_id"] = None
                l_shape["description"] = ""
                l_shape["shape_type"] = "polygon"
                l_shape["flags"] = {}
                shapes.append(l_shape)
    annotations["shapes"] = shapes
    return annotations


yolo_annotations_folder = filedialog.askdirectory(title='Select the folder containing YOLOv8 annotations')
destination_folder = filedialog.askdirectory(title='Select the destination folder where labelMe annotations are saved')

if not os.path.exists(yolo_annotations_folder):
    print('YOLO folder does not exist')

patients = os.listdir(destination_folder)
for patient in patients:
    json_files = glob.glob(os.path.join(destination_folder, patient, '*.json'))
    for json_file in json_files:
        if os.path.exists(os.path.join(yolo_annotations_folder, patient, os.path.basename(json_file))):
            yolo_annotations = json.load(open(os.path.join(yolo_annotations_folder, patient, os.path.basename(json_file))))
            labelme_annotations = json.load(open(json_file))
            annotations = merge_annotations(labelme_annotations, yolo_annotations)
            print(annotations)
            with open(json_file, 'w') as outfile:
                json.dump(annotations, outfile, indent=4)