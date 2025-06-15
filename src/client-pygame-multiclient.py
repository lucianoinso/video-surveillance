from flask import Flask, Response
import pygame.camera
import pygame.image
from PIL import Image
import io
import threading
import time

app = Flask(__name__)

# Camera setup
pygame.camera.init()
CAMERA_SIZE = (640, 480)
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], CAMERA_SIZE)
cam.start()

# Shared latest frame
latest_frame = None
lock = threading.Lock()

def capture_frames():
    global latest_frame
    while True:
        surface = cam.get_image()
        pil_img = pygame.image.tostring(surface, 'RGB')
        img = Image.frombytes('RGB', surface.get_size(), pil_img)
        buf = io.BytesIO()
        img.save(buf, format='JPEG')
        with lock:
            latest_frame = buf.getvalue()
        time.sleep(1 / 15)  # Capture at ~15 FPS

# Start background capture thread
threading.Thread(target=capture_frames, daemon=True).start()

def generate():
    while True:
        with lock:
            if latest_frame is None:
                continue
            frame = latest_frame
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )
        time.sleep(1 / 15)

@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '<img src="/video">'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)

