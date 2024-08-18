import cv2

cap = cv2.VideoCapture(0)

while True:
    # Чтение кадра с камеры
    ret, frame = cap.read()

    if not ret:
        break

    # Выполните предсказание на кадре
    results = model(frame, conf=0.95, iou=0.7)

    # Получите изображение с нарисованными bounding box'ами
    annotated_frame = results[0].plot()

    # Отобразите кадр
    cv2.imshow('YOLO Real-Time Detection', annotated_frame)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
