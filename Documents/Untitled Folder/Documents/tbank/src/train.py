from ultralytics import YOLO
import torch





model = YOLO('yolov8n.pt')

if torch.cuda.is_available():
    print("-------cuda is available---------")
else:
    print("-------------cuda is not available----------")


model.train(data='../data_config.yaml', epochs=60, imgsz=640, device='0', batch=16, augment=False)


'''result = model.predict('../dataset/images/test/0a2d9334483d2463efbf4c622a542f10.jpg',
              imgsz=640,
              conf=0.25,
              iou=0.45,
              device='0')

result.show()
'''

print("hello nigz")