"""
Raw Data means the original Dicom images.
This Program extract the pixel values from the Dicom file. Then normalize it using the
'WindowCenter' and 'WindowWidth' parameters from the Dicom file.
Each patient folder is named after the patient's name. Then the name is anonymized by hashing.

The Dicom images folder should have the following structure:

DicomImages/
    patient1/
        image1.dcm
        image2.dcm
        ...
    patient2/
        image1.dcm
        image2.dcm
        ...
    ...

The structure of the output folders:

Dataset/
    images/
        patient1/
            image1.png
            image2.png
            ...
        patient2/
            image1.png
            image2.png
            ....
    annotations/
        patient1/
            image1.json
            image2.json
            ...
        patient2/
            image1.json
            image2.json
            ....
"""

import pydicom
import hashlib
import cv2
import os
import numpy as np
import glob
from tkinter import filedialog as fd
import shutil

root_path = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets"
# dataset_path = "Dataset_0_1"
processed_data_folder = os.path.join(root_path,"processed_data")  # After the raw data is extracted and annonymised, the original data will be moved into this folder.
if not os.path.exists(processed_data_folder):
    os.makedirs(processed_data_folder,exist_ok=True)
images_dir = os.path.join(root_path, "Segment_AI_dataset/images")
if not os.path.exists(images_dir):
    os.makedirs(images_dir, exist_ok=True)
annotations_dir =images_dir
# raw_data_folder = fd.askdirectory(title="Select the Dicom images' folder")
raw_data_folder = os.path.join(root_path, "raw_dicom_data") # This folder is the place to put the original unprocessed images. these images will be moved to processed_data_folder after processing
patients = os.listdir(raw_data_folder)
print(patients)
for patient in patients:
    dcm_files = glob.glob(os.path.join(raw_data_folder, patient, '*.dcm'))
    print(dcm_files)
    postfix =0
    for dcm_file in dcm_files:
        print(dcm_file)
        dcm_content = pydicom.dcmread(dcm_file)
        p_name = str(dcm_content[0x0010,0x0010].value).replace("^", " ")
        h = hashlib.blake2b(digest_size=10)
        h.update(bytes(p_name, 'utf-8'))
        p_name_hash = h.hexdigest()
        print(p_name_hash)
        if not os.path.exists(os.path.join(images_dir, str(p_name_hash))):
            os.makedirs(os.path.join(images_dir, str(p_name_hash)))
        # Get the image and bring the pixel values to normal range
        img_pixel = dcm_content.pixel_array.astype(np.float16)
        img_pixel = (img_pixel - dcm_content.WindowCenter + 0.5 * dcm_content.WindowWidth) / dcm_content.WindowWidth
        img_pixel[img_pixel < 0] = 0
        img_pixel[img_pixel > 1] = 1
        img_pixel = img_pixel * 255
        img_pixel = img_pixel.astype(np.uint8)
        if hasattr(dcm_content, "PresentationLUTShape"):
            if dcm_content.PresentationLUTShape == 'INVERSE':
                img_pixel = 255 - img_pixel
        laterality = dcm_content.SeriesDescription
        laterality = laterality.replace(" ", "")
        image_name = str(p_name_hash) + '_' + laterality + '_' + str(postfix) + '.png'
        # if os.path.exists(os.path.join(images_dir, str(p_name_hash), image_name)):
        #     image_name = str(p_name_hash) + '_' + laterality + '_' + str(postfix+1) + '.png'
        image_path = os.path.join(images_dir, str(p_name_hash), image_name)
        cv2.imwrite(image_path, img_pixel)
        source_json_path = dcm_file.split('.')[0] + '.json'
        if os.path.exists(source_json_path):
            dest_json_file_name = image_name.split('.')[0]+'.json'
            if not os.path.exists(os.path.join(annotations_dir, str(p_name_hash))):
                os.makedirs(os.path.join(annotations_dir, str(p_name_hash)))
            shutil.copy(source_json_path, os.path.join(annotations_dir, str(p_name_hash), dest_json_file_name))
    shutil.move(os.path.join(raw_data_folder, patient), processed_data_folder)