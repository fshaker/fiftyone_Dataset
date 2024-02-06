import fiftyone as fo
import os
import json
import numpy as np
import cv2

def add_predictions(dataset_name, predictions_path, predictions_name):
    dataset = fo.load_dataset(dataset_name)
    # print(dataset)
    for sample in dataset:
        # print(sample)
        img_width = sample["metadata"]["width"]
        img_height = sample["metadata"]["height"]
        image_name = os.path.basename(sample["filepath"])
        # print("image name :", image_name)
        # print("predictions_path", predictions_path)
        if os.path.exists(predictions_path):
            detections = []
            if "_" in image_name:
                sample_predictions_path = os.path.join(predictions_path, image_name.split('_')[0])
            else:
                patient = os.path.split(sample["filepath"])[-2]
                patient = patient.split('\\')[-1]
                # print(patient)
                sample_predictions_path = os.path.join(predictions_path, patient)
                # print("sample_predictions_path", sample_predictions_path)
            predictions = os.path.join(sample_predictions_path, image_name.split('.')[0] + ".json")
            # print("predictions: ", predictions)
            if os.path.exists(predictions):
                predictions_content = json.load(open(predictions, 'r'))
            else:
                continue
            # print("sample", sample)
            for shape in predictions_content["shapes"]:
                # print("shape", shape)
                label = shape['label']
                [x1, y1, x2, y2] = shape['bbox']
                bounding_box = [float(x1) / img_width, float(y1) / img_height, float(x2 - x1) / img_width,
                                float(y2 - y1) / img_height]
                mask = np.array(shape['mask']) > 0
                if len(mask.shape) < 2:
                    mask = np.zeros((10, 10))
                elif (mask.shape[0]) == 0 or (mask.shape[1]) == 0:
                    mask = np.zeros((10, 10))
                confidence = float(shape['confidence'])
                detections.append(
                    fo.Detection(label=label, bounding_box=bounding_box, mask=mask, confidence=confidence))
            sample[predictions_name] = fo.Detections(detections=detections)
            # print("sample after: ",sample)
            sample.save()


if __name__ == "__main__":
    # predictions_pth =  r"C:\Users\Admin\Documents\VidaMedicals\Codes\BreastCancerDetecton\results\mass_detection_1024_to_512\output\RUN_1_mvitv2_big_giou\inference_output"
    predictions_pth = r"C:\Users\Admin\Documents\VidaMedicals\Codes\BreastCancerDetecton\results\whole_images\output\RUN_1_mvitv2_big_giou\inference_output_5"
    print("start")
    add_predictions(dataset_name="SegmentAnnotate",
                    # dataset_split="test",
                    predictions_path=predictions_pth,
                    predictions_name="mass_detections_whole_image")
