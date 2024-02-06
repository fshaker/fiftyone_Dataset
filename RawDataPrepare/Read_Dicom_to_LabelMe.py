import json
import tkinter.filedialog
import cv2
import pydicom
import numpy as np
import os
import glob


def get_image_from_dicom(dicom_file):
    dcm_content = pydicom.dcmread(dicom_file)
    ###########################################################################
    # Get the image and bring the pixel values to normal range
    ###########################################################################
    img_pixel = dcm_content.pixel_array.astype(np.float16)
    img_pixel = (img_pixel - dcm_content.WindowCenter + 0.5 * dcm_content.WindowWidth) / dcm_content.WindowWidth
    img_pixel[img_pixel < 0] = 0
    img_pixel[img_pixel > 1] = 1
    img_pixel = img_pixel * 255
    img_pixel = img_pixel.astype(np.uint8)
    if hasattr(dcm_content, "PresentationLUTShape"):
        if dcm_content.PresentationLUTShape == 'INVERSE':
            img_pixel = 255 - img_pixel
    # laterality = dcm_content.SeriesDescription
    # print(laterality.replace(" ", "_"))

    # the format of image name is the combination of Patient ID and Laterality of the image, i.e. 000001_L_CC
    # we use 6 digits for patient id

    return img_pixel
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
shape =  {
                "label": "No Finding",
                "points": [

                ],
                "group_id": None,
                "description": "",
                "shape_type": "polygon",
                "flags": {}
            }
def get_json_annotation(dicom_file):
    dcm_content = pydicom.dcmread(dicom_file)
    json_content = {}
    json_content["version"] = "5.2.1"
    json_content["flags"] = flags
    json_content["shapes"]=[shape]
    json_content["imagePath"]=dicom_file.split('.')[0]+".png"
    json_content["imageData"]= None
    return json_content

import tkinter as tk

images_path = tkinter.filedialog.askdirectory(title="Select the dicom folder")
subfolders = os.listdir(images_path)
for folder in subfolders:
    dicom_files = glob.glob(os.path.join(images_path, folder, "*.dicom"))
    for dicom_file in dicom_files:
        image_pixel = get_image_from_dicom(dicom_file = dicom_file)
        json_annotation = get_json_annotation(dicom_file = dicom_file)
        json_annotation["imageHeight"] = image_pixel.shape[1]
        json_annotation["imageWidth"] = image_pixel.shape[0]
        outfile = dicom_file.split('.')[0]+".json"
        with open(outfile, "w") as file:
            json.dump(json_annotation, file, sort_keys=False, indent=4)
        cv2.imwrite(dicom_file.split('.')[0]+".png", image_pixel)
