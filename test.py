from ultralytics import YOLO
import cv2

# Загрузите модель YOLO
model = YOLO('yolov8n.pt')

# Загрузите другое изображение для тестирования
img = cv2.imread('images/bottle.jpg')

# Выполните предсказание с порогами уверенности и NMS
results = model(img, conf=0.7)

# Отобразите изображение с боксами
annotated_frame = results[0].plot()
cv2.imshow('pic', annotated_frame)
cv2.waitKey(0)
# import torch
# print(torch.cuda.is_available())
