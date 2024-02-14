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
import os
import shutil
from tkinter import filedialog


source_data_path = filedialog.askdirectory(title='Select source data directory')
destination_data_path = filedialog.askdirectory(title='Select anonymized data directory')
patients = os.listdir(source_data_path)
print(patients)
data_set_names_list_file = os.path.join(destination_data_path, 'data_set_names_list.csv')

for patient in patients:
    # For each patient,
    files = os.listdir(os.path.join(source_data_path, patient))
    postfix = 0
    for file in files:
        if '.' not in file:
            dcm_path = os.path.join(source_data_path, patient, file)
            img_path = os.path.join(source_data_path, patient, file+'.png')
            json_path = os.path.join(source_data_path, patient, file+'.json')
            # print(dcm_files)
            dcm_content = pydicom.dcmread(dcm_path)
            # print(dcm_content.PhotometricInterpretation)
            # print(dcm_content)
            p_name = str(dcm_content[0x0010, 0x0010].value).replace("^", " ")
            acquisition_date = str(dcm_content.AcquisitionDate)
            h = hashlib.blake2b(digest_size=10)
            h.update(bytes(p_name, 'utf-8'))
            h.update(bytes(acquisition_date, 'utf-8'))
            p_name_hash = h.hexdigest()
            # print(p_name_hash)
            if not os.path.exists(os.path.join(destination_data_path, str(p_name_hash))):
                os.makedirs(os.path.join(destination_data_path, str(p_name_hash)))
            laterality = dcm_content.SeriesDescription
            laterality = laterality.replace(" ", "")
            image_name = str(p_name_hash) + '_' + laterality + '_' + str(postfix) + '.png'
            json_name = str(p_name_hash) + '_' + laterality + '_' + str(postfix) + '.json'
            shutil.copy(img_path, os.path.join(destination_data_path, str(p_name_hash), image_name))
            shutil.copy(json_path, os.path.join(destination_data_path, str(p_name_hash), json_name))
    with open(data_set_names_list_file, 'a') as f:
        f.write(p_name+ ','+acquisition_date+ ','+ p_name_hash+'\n')