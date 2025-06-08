from flask import Flask, Response
import cv2

app = Flask(__name__)
cap = cv2.VideoCapture(2)  # use /dev/video2

# Stream properties
WIDTH = 320
HEIGHT = 240
IMAGE_QUALITY = 80 # from 0 to 100

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.resize(frame, (WIDTH, HEIGHT))
            # Flip if necessary (my laptop flips the input in linux)
            frame = cv2.flip(frame, 0)

            # Encode as JPEG
            ret, buffer = cv2.imencode('.jpg', frame,
                                       [cv2.IMWRITE_JPEG_QUALITY, IMAGE_QUALITY])
            if not ret:
                continue

            # Yield frame in multipart format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)

