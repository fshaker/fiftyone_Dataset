import torch
import torchvision
from fiftyone import ViewField as F
import fiftyone as fo
import fiftyone.zoo as foz


# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
# model.to(device)
# model.eval()
#
# print("model ready")



name = "SegmentAnnotate"
dataset = fo.load_dataset(name)
# high_conf_view = dataset.filter_labels('predictions', F("confidence")>0.5, only_matches=False)
# results = high_conf_view.evaluate_detections(
#     "predictions",
#     gt_field="ground_truth",
#     eval_key="eval",
#     compute_mAP=True)
# counts = high_conf_view.count_values("ground_truth.detections.label")
# classes_top4 = sorted(counts, key=counts.get, reverse=True)[:4]
# results.print_report(classes_top4)

session = fo.launch_app(dataset)
session.wait()
