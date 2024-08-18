import cv2
import threading
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
from ultralytics import YOLO
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

# Подключение статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Загрузка модели YOLO
model = YOLO('models/yolov8n.pt')

# Глобальная переменная для хранения видеопотока
video_capture = None
is_running = False
frame_lock = threading.Lock()

def generate_frames():
    global video_capture, is_running
    while is_running:
        with frame_lock:
            success, frame = video_capture.read()
        if not success:
            break

        # Применяем модель YOLOv8 к каждому кадру
        results = model(frame, conf=0.4)
        annotated_frame = results[0].plot()

        # Кодирование кадра в формат JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()

        # Генерация потока с кадрами
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.post("/start_camera")
def start_camera():
    global video_capture, is_running
    if not is_running:
        video_capture = cv2.VideoCapture(0)
        is_running = True
        return {"message": "Camera started"}
    return {"message": "Camera is already running"}

@app.post("/stop_camera")
def stop_camera():
    global is_running
    if is_running:
        is_running = False
        with frame_lock:
            video_capture.release()
        return {"message": "Camera stopped"}
    return {"message": "Camera is not running"}

@app.on_event("shutdown")
def shutdown_event():
    global video_capture, is_running
    if is_running and video_capture:
        video_capture.release()
        is_running = False
