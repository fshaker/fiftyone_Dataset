import os
import glob
import json
import shutil
import argparse

import cv2
import numpy as np

def extract_subgroups(input):
    subgroup_mapper = {
        'ca': {
            'morphology':{
                1 : 'benign',
                2 : 'amorphous',
                3 : 'coarse',
                4 : 'pleiomorphic',
                5 : 'linear/branching',
            },
            'benign':{
                0 : 'none',
                1 : 'skin',
                2 : 'vascular',
                3 : 'coarse',
                4 : 'rod-like',
                5 : 'round',
                6 : 'rim',
                7 : 'dystrophic',
                8 : 'milk',
                9 : 'suture',
            },
            'distribution':{
                0 : 'none',
                1 : 'diffuse',
                2 : 'regional',
                3 : 'grouped',
                4 : 'linear',
                5 : 'segmental',
            },
            'bi-rads' : {
                0 : '0',
                1 : '1',
                2 : '2',
                3 : '3',
                4 : '4',
                41 : '4A',
                42 : '4B',
                43 : '4C',
                5 : '5',
                6 : '6',
            },
        },
        'mass': {
            'shape' : {
                1 : 'oval',
                2 : 'round',
                3 : 'irregular',
            },
            'margin' : {
                1 : 'circumscribed',
                2 : 'obscured',
                3 : 'microlobulated',
                4 : 'indistinct',
                5 : 'spiculated',
            },
            'density' : {
                1 : 'fat',
                2 : 'low',
                3 : 'equal',
                4 : 'high',
            },
            'bi-rads' : {
                0 : '0',
                1 : '1',
                2 : '2',
                3 : '3',
                4 : '4',
                5 : '4A',
                6 : '4B',
                7 : '4C',
                8 : '5',
                9 : '6',
            },
        },
        'lymph node' : {
            1 : 'benign',
            2 : 'suspicious',
            3 : 'b',
            4 : 's',
        },
        'asymmetry' : {
            'morphology' : {
                1 : 'asymmetry',
                2 : 'global',
                3 : 'focal',
                4 : 'develop',
            },
            'bi-rads' : {
                0 : '0',
                1 : '1',
                2 : '2',
                3 : '3',
                4 : '4',
                5 : '4A',
                6 : '4B',
                7 : '4C',
                8 : '5',
                9 : '6',
            },
        },
    }

def extract_category(name):
    if "c" in name or "C" in name:
        return "Calcification"
    elif "m" in name or "M" in name:
        return "Mass"
    elif "a" in name or "A" in name:
        return "Asymmetries"
    else:
        return "Suspicious"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset-dir",
        type=str,
        default=None,
        help='Path to dataset directory'
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help='Path to converted dataset directory'
    )

    output_dict = {
        "licenses": [
            {
                "name": "",
                "id": 0,
                "url": ""
            }
        ],
        "info": {
            "contributor": "",
            "date_created": "",
            "description": "",
            "url": "",
            "version": "",
            "year": ""
        },
        "categories": [
            {
                "id": 1,
                "name": "Calcification",
                "supercategory": ""
            },
            {
                "id": 2,
                "name": "Mass",
                "supercategory": ""
            },
            {
                "id": 3,
                "name": "Asymmetries",
                "supercategory": "",
            },
            {
                "id": 4,
                "name": "Suspicious",
                "supercategory": "",
            }
        ],
        "images": [],
        "annotations": [],
    }

    args = parser.parse_args()

    output_home_dir = args.output_dir
    output_dir = "datasets"
    images_path = "images"
    os.makedirs(output_home_dir, exist_ok=True)
    os.makedirs(os.path.join(output_home_dir, output_dir), exist_ok=True)
    os.makedirs(os.path.join(output_home_dir, output_dir, images_path), exist_ok=True)

    for idx, file in enumerate(sorted(glob.glob(os.path.join(args.dataset_dir, '*', '*.json')))):
        ann = json.load(open(file))
        output_dict["images"].append(
            {
                "id": idx,
                "width": ann["imageWidth"],
                "height": ann["imageHeight"],
                "file_name": os.path.join(output_dir, images_path, file.split(os.sep)[-2], file.split(os.sep)[-1].replace(".json", ".png")),
                "license": 0,
                "flickr_url": "",
                "coco_url": "",
                "date_captured": 0
            }
        )
        
        if not os.path.exists(os.path.join(output_home_dir, output_dir, images_path, file.split(os.sep)[-2])):
            os.mkdir(os.path.join(output_home_dir, output_dir, images_path, file.split(os.sep)[-2]))
        
        shutil.copy(
            file.replace(".json", ".png"),
            os.path.join(output_home_dir, output_dir, images_path, file.split(os.sep)[-2], file.split(os.sep)[-1].replace(".json", ".png"))
        )
        for jdx, shape in enumerate(ann["shapes"]):
            points = np.array(shape['points']).reshape(-1, 2).astype(np.float32)
            if points.shape[0] <= 3:
                continue
            px = points[:, 0]
            py = points[:, 1]
            px = px.tolist()
            py = py.tolist()
            poly = [(x-0.5, y) for x, y in zip(px, py)]
            poly = [p for x in poly for p in x]
            output_dict["annotations"].append(
                {
                    "id": jdx,
                    "image_id": idx,
                    "category_id": [i["id"] for i in output_dict['categories'] if i["name"] == extract_category(shape["label"])][0],
                    "segmentation": [poly],
                    "area": cv2.contourArea(points),
                    "bbox": [np.min(px), np.min(py), np.max(px)-np.min(px), np.max(py)-np.min(py)],
                    "iscrowd": 0,
                }
            )
    os.mkdir(os.path.join(output_home_dir, output_dir, "annotations"))
    with open(os.path.join(output_home_dir, output_dir, "annotations", "instances_default.json"), "w") as f:
        json.dump(output_dict, f, sort_keys=False, indent=4)