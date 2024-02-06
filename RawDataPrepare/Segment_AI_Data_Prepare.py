"""
Raw Data means the original Dicom images.
This Program extract the pixel values from the Dicom file. Then normalize it using the
'WindowCenter' and 'WindowWidth' parameters from the Dicom file.
Each patient folder is named after the patient's name. Then the name is anonymized by hashing.

UPDATE: The acquisition date of the dicom data is also added to the name of folder before hashing

The Dicom images folder should have the following structure:

raw_dicom_data/
    patient1/
        image1.dcm
        image2.dcm
        ...
    patient2/
        image1.dcm
        image2.dcm
        ...
    ...
if there is annotations in the same folder as raw_dicom_data, those annotations are also added to the
"""

import pydicom
import hashlib
import cv2
import os
import numpy as np
import shutil


data_set_names_list_file = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets\Processed_data_info.csv"
root_path = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets"

processed_data_folder = os.path.join(root_path,"processed_dicom_data")  # After the raw data is extracted and annonymised, the original data will be moved into this folder.
if not os.path.exists(processed_data_folder):
    os.makedirs(processed_data_folder,exist_ok=True)
# images_dir is the folder that the extracted images will be saved
Prepared_data_dir = os.path.join(root_path, "Segment_AI_dataset\images")
if not os.path.exists(Prepared_data_dir):
    os.makedirs(Prepared_data_dir, exist_ok=True)
annotations_dir =Prepared_data_dir
# raw_data_folder = fd.askdirectory(title="Select the Dicom images' folder")
raw_data_folder = os.path.join(root_path, "raw_dicom_data") # This folder is the place to put the original unprocessed images. these images will be moved to processed_data_folder after processing
print(raw_data_folder)
patients = os.listdir(raw_data_folder)
print(patients)
for patient in patients:
    # For each patient,
    dcm_files = os.listdir(os.path.join(raw_data_folder, patient))
    postfix =0
    p_name = ''
    acquisition_date = ''
    p_name_hash = ''
    for dcm_file in dcm_files:

        dcm_content = pydicom.dcmread(os.path.join(raw_data_folder, patient, dcm_file))
        print(dcm_content.PhotometricInterpretation)
        p_name = str(dcm_content[0x0010, 0x0010].value).replace("^", " ")
        acquisition_date = str(dcm_content.AcquisitionDate)
        h = hashlib.blake2b(digest_size=10)
        h.update(bytes(p_name, 'utf-8'))
        h.update(bytes(acquisition_date, 'utf-8'))
        p_name_hash = h.hexdigest()
        # print(p_name_hash)
        if not os.path.exists(os.path.join(Prepared_data_dir, str(p_name_hash))):
            os.makedirs(os.path.join(Prepared_data_dir, str(p_name_hash)))
        # Get the image and bring the pixel values to normal range
        img_pixel = dcm_content.pixel_array
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
        image_path = os.path.join(Prepared_data_dir, str(p_name_hash), image_name)
        cv2.imwrite(image_path, img_pixel)
        source_json_path = dcm_file.split('.')[0] + '.json'
        if os.path.exists(source_json_path):
            dest_json_file_name = image_name.split('.')[0]+'.json'
            if not os.path.exists(os.path.join(annotations_dir, str(p_name_hash))):
                os.makedirs(os.path.join(annotations_dir, str(p_name_hash)))
            shutil.copy(source_json_path, os.path.join(annotations_dir, str(p_name_hash), dest_json_file_name))
        # save the name of the patient and the corresponding folder name:
    with open(data_set_names_list_file, 'a') as f:
        f.write(p_name+ ','+acquisition_date+ ','+ p_name_hash+'\n')
    shutil.move(os.path.join(raw_data_folder, patient), processed_data_folder)