import cv2
from ultralytics import YOLO

# Загрузите модель YOLO
model = YOLO('models/yolov8n.pt')

# Откройте видеопоток с камеры (0 - это индекс камеры по умолчанию)
cap = cv2.VideoCapture(0)

while True:
    # Чтение кадра с камеры
    ret, frame = cap.read()

    if not ret:
        break

    # Выполните предсказание на кадре
    results = model(frame, conf=0.4)

    # Получите изображение с нарисованными bounding box'ами
    annotated_frame = results[0].plot()

    # Отобразите кадр
    cv2.imshow('YOLO Real-Time Detection', annotated_frame)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение захвата и закрытие всех окон
cap.release()
cv2.destroyAllWindows()
