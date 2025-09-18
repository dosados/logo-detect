import os
from ultralytics import YOLO
import cv2

model_path = "src/runs/detect/train14/weights/best.pt"  
images_dir = "full_dataset/images/train"   
labels_dir = "full_dataset?labels/train"   

model = YOLO(model_path)

image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

for img_name in image_files:
    img_path = os.path.join(images_dir, img_name)
    img = cv2.imread(img_path)
    h, w = img.shape[:2]


    results = model(img_path)[0]


    label_path = os.path.join(labels_dir, os.path.splitext(img_name)[0] + ".txt")

    with open(label_path, "w") as f:
        for box in results.boxes:
            cls = int(box.cls[0])  
            x1, y1, x2, y2 = box.xyxy[0]  

            x_center = ((x1 + x2) / 2) / w
            y_center = ((y1 + y2) / 2) / h
            width = (x2 - x1) / w
            height = (y2 - y1) / h

            f.write(f"{cls} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

print("✅ Лейблы сохранены в", labels_dir)
