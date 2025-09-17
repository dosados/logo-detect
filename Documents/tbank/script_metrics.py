from ultralytics import YOLO
import os
import glob
import json
from pathlib import Path
from sklearn.metrics import precision_score, recall_score
import numpy as np

# Путь к модели YOLOv8
MODEL_PATH = "/home/timofey/Documents/tbank/src/runs/detect/train14/weights"  # твой вес модели
TEST_IMAGES_DIR = "/home/timofey/Documents/tbank/dataset/images/val"  # папка с тестовыми изображениями
ANNOTATIONS_DIR = "/home/timofey/Documents/tbank/dataset/labels/val"  # папка с аннотациями в формате YOLO

# Загрузка модели
model = YOLO(MODEL_PATH)

# Функция для чтения аннотаций YOLO
def read_yolo_labels(label_path):
    boxes = []
    with open(label_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            cls, x_center, y_center, w, h = map(float, line.strip().split())
            x_min = x_center - w/2
            y_min = y_center - h/2
            x_max = x_center + w/2
            y_max = y_center + h/2
            boxes.append([int(cls), x_min, y_min, x_max, y_max])
    return boxes

# IoU функция
def iou(box1, box2):
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)
    box1_area = (box1[2]-box1[0])*(box1[3]-box1[1])
    box2_area = (box2[2]-box2[0])*(box2[3]-box2[1])
    return inter_area / (box1_area + box2_area - inter_area + 1e-6)

# Порог для IoU
IOU_THRESHOLD = 0.5

# Сбор всех изображений
image_paths = glob.glob(os.path.join(TEST_IMAGES_DIR, "*.jpg"))

all_precisions = []
all_recalls = []

for img_path in image_paths:
    img_name = Path(img_path).stem
    label_path = os.path.join(ANNOTATIONS_DIR, img_name + ".txt")
    
    gt_boxes = read_yolo_labels(label_path)
    
    # Предсказания модели
    results = model.predict(img_path)
    pred_boxes = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cls = int(box.cls[0])
            pred_boxes.append([cls, x1, y1, x2, y2])
    
    # Сравнение предсказаний с GT
    tp, fp, fn = 0, 0, 0
    matched = []
    for pred in pred_boxes:
        found = False
        for i, gt in enumerate(gt_boxes):
            if i in matched:
                continue
            if pred[0] == gt[0] and iou(pred[1:], gt[1:]) >= IOU_THRESHOLD:
                tp += 1
                matched.append(i)
                found = True
                break
        if not found:
            fp += 1
    fn = len(gt_boxes) - len(matched)
    
    precision = tp / (tp + fp + 1e-6)
    recall = tp / (tp + fn + 1e-6)
    
    all_precisions.append(precision)
    all_recalls.append(recall)

# Средние метрики
mean_precision = np.mean(all_precisions)
mean_recall = np.mean(all_recalls)

print(f"Mean Precision: {mean_precision:.4f}")
print(f"Mean Recall: {mean_recall:.4f}")