import cv2

# Replace with your local IP
mjpeg_url = "http://172.18.0.1:8080/"

cap = cv2.VideoCapture(mjpeg_url)

if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

def receive_video():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # frame = cv2.flip(frame, 0)
        cv2.imshow("MJPEG Stream", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
    try:
        receive_video()
    except Exception as e:
        print(e)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
