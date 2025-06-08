import cv2
from datetime import datetime
from time import sleep

# Replace with the server's IP
STREAM_URI = "http://192.168.100.4:8080/"
WIDTH = 240
TEXT_POSITION = (2, WIDTH - 5)

def receive_video():
    while True:
        try:
            cap = cv2.VideoCapture(STREAM_URI)
            if not cap.isOpened():
                raise RuntimeError("Failed to open video stream")

            while True:
                ret, frame = cap.read()
                if not ret:
                    raise Exception("Stream read failed")

                date_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

                cv2.putText(frame, date_str, TEXT_POSITION,
                    fontFace=cv2.FONT_HERSHEY_DUPLEX,
                    fontScale=0.5, color=(0, 255, 0), thickness=1,
                    lineType=cv2.LINE_AA)

                cv2.imshow("MJPEG Stream", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    raise KeyboardInterrupt

        except Exception as e:
            print(f"[ERROR] {e}")
            print("Retrying in 5 seconds...")
            cap.release()
            sleep(5)
        except KeyboardInterrupt:
            print("Exiting...")
            cap.release()
            cv2.destroyAllWindows()
            break

def main():
    print(f"Streaming from: {STREAM_URI}")
    print("Press \"q\" key to exit")
    receive_video()

if __name__ == '__main__':
    main()
