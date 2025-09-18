from ultralytics import YOLO
import torch


model = YOLO('yolov8n.pt')

if torch.cuda.is_available():
    print("-------cuda is available---------")
else:
    print("-------------cuda is not available----------")


model.train(data='../data_config.yaml', epochs=60, imgsz=640, device='0', batch=16, augment=False)


print("hello nigz")