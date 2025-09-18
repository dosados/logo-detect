from ultralytics import YOLO

MODEL_PATH = "../weights/best.pt"

model = YOLO(MODEL_PATH)

metrics = model.val(data="/home/timofey/Documents/tbank/data.yaml", imgsz=640)

print("mAP@0.5:", metrics.box.map50)
print("mAP@0.5:0.95:", metrics.box.map)
print("Precision:", metrics.box.p)   # массив по классам
print("Recall:", metrics.box.r)      # массив по классам