"""
This Script is used to convert
"""

import glob
import os
import pydicom
from PIL import Image
from tkinter import filedialog
import hashlib

jpeg_path = filedialog.askdirectory(title='Select the jpeg images root directory')
dcm_path = filedialog.askdirectory(title='Select the dicom images root directory')
png_path = filedialog.askdirectory(title='Select the destination data folder')
jpeg_files = glob.glob(os.path.join(jpeg_path, '*.jpg'))
patients = os.listdir(dcm_path)
data_set_names_list_file = os.path.join(png_path, 'data_set_names_list.csv')
os.makedirs(png_path, exist_ok=True)
for patient in patients:
    postfix = 0
    dcm_files = os.listdir(os.path.join(dcm_path, patient))
    p_name = ''
    acquisition_date = ''
    p_name_hash = ''
    for dcm_file in dcm_files:
        dcm_content = pydicom.dcmread(os.path.join(dcm_path, patient, dcm_file))
        p_name = str(dcm_content[0x0010, 0x0010].value).replace("^", " ")
        acquisition_date = str(dcm_content.AcquisitionDate)
        h = hashlib.blake2b(digest_size=10)
        h.update(bytes(p_name, 'utf-8'))
        h.update(bytes(acquisition_date, 'utf-8'))
        p_name_hash = h.hexdigest()
        if not os.path.exists(os.path.join(png_path, str(p_name_hash))):
            os.makedirs(os.path.join(png_path, str(p_name_hash)))
        laterality = dcm_content.SeriesDescription
        laterality = laterality.replace(" ", "")
        image_name = str(p_name_hash) + '_' + laterality + '_' + str(postfix) + '.png'
        jpeg_image = Image.open(os.path.join(jpeg_path, patient, dcm_file+'.jpg')) # the name of jpeg files are the same as the dicom files
        jpeg_image.save(os.path.join(png_path, p_name_hash, image_name)) # converts to png file
    with open(data_set_names_list_file, 'a') as f:
        f.write(p_name + ',' + acquisition_date + ',' + p_name_hash + '\n')