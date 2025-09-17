from ultralytics import YOLO
import torch
import cv2
import os
import matplotlib as plt



# Путь к сохранённым весам
weights_path = "runs/detect/train14/weights/best.pt"  

# Загружаем модель
model = YOLO(weights_path)

# Проверяем доступность CUDA
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")


test_image_dir = "../full_dataset/data_sirius"

k = 0
for filename in os.listdir(test_image_dir):
    if k > 40:
        break
    image_path = os.path.join(test_image_dir, filename)
    result = model.predict(source=image_path, device=device, imgsz=640)
    annotated_img = result[0].plot()
    cv2.imwrite(f"../checks/annotated_image{k}.jpg", annotated_img)

    k += 1


