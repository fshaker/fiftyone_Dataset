import fiftyone as fo
import os
import json
import numpy as np
import cv2

name = "SegmentAnnotate"
dataset = fo.load_dataset(name)
for sample in dataset:
    image_folder_name = os.path.basename(os.path.dirname(sample["filepath"]))
    annotations_path = sample["filepath"].split('.')[0]+'.json'
    # annotations_path = os.path.join(images_dir, image_folder_name, annotations_file)
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
            #create the mask. for cv2, floodfill function,
            # the mask should be 2 pixel wider and 2 pixel taller that the contour
            # mask_with_contours = np.zeros([round(y2-y1), round(x2-x1)], np.uint8)  # numpy.zeros([100, 100],numpy.uint8)
            mask = np.zeros([round(y2-y1)+2, round(x2-x1)+2], np.uint8)
            polygon = np.array((polyline - [x1-1, y1-1]), dtype=np.int32) #numpy.array([[1,1],[10,50],[50,50]], dtype=numpy.int32)
            # print(mask.shape)
            # print(mask_with_contours.shape)
            print((int((y2-y1)//2), int((x2-x1)//2)))
            cv2.drawContours(mask, [polygon],-1,(255),1)
            # find a seed point inside the polygon
            # y = int(mask_with_contours.shape[0]//2)
            # row = mask_with_contours[y,:]
            # print(row)
            # inds = [idx for idx, val in enumerate(row) if val!=0]
            # print(inds)
            # x = int((inds[0] + inds[-1])//2)
            # cv2.floodFill(mask_with_contours, mask, (x, y), 255)
            mask = mask>0
            # polygon = (np.array(polyline)-[x1, y1])/((x2-x1),(y2-y1))
            # print(polygon)
            bounding_box = [float(x1) / img_width, float(y1) / img_height, float(x2 - x1) / img_width,
                            float(y2 - y1) / img_height]
            detections.append(fo.Detection(label=label,
                                           bounding_box=bounding_box, mask = mask))
    sample["ground_truth"] = fo.Detections(detections=detections)
    sample.save()
