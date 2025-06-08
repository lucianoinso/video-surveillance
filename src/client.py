from datetime import datetime
import time

import cv2

from tensorflow.keras.applications.mobilenet import MobileNet

from classifier import classify


# Replace with the server's IP
STREAM_URI = "http://192.168.100.4:8080/"
WIDTH = 240
DATE_POSITION = (2, WIDTH - 5)
CLASS_POSITION = (2, 20)

def receive_video():
    while True:
        try:
            model = MobileNet(weights='imagenet')
            cap = cv2.VideoCapture(STREAM_URI)
            if not cap.isOpened():
                raise RuntimeError("Failed to open video stream")
            else:
                print(f"Connection established, " \
                      f"streaming from: {STREAM_URI}")

            last_called = time.time()
            class_name, confidence_level = ("", 0)

            while True:
                ret, frame = cap.read()
                if not ret:
                    raise Exception("Stream read failed")

                date_str = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

                # Classify after 250 ms
                if time.time() - last_called >= 1:
                    class_name, confidence_level = classify(model, frame)
                    last_called = time.time()

                if confidence_level > 80:
                    text_color = (255, 0, 0)
                else:
                    text_color = (0, 0, 255)

                cv2.putText(frame, str(f"{confidence_level:.2f}% {class_name}"),
                            CLASS_POSITION, cv2.FONT_HERSHEY_DUPLEX,
                            fontScale=0.5, color=text_color, thickness=1,
                            lineType=cv2.LINE_AA)

                cv2.putText(frame, date_str, DATE_POSITION,
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
            time.sleep(5)
        except KeyboardInterrupt:
            print("Exiting...")
            cap.release()
            cv2.destroyAllWindows()
            break

def main():
    print("Press \"q\" key to exit")
    receive_video()

if __name__ == '__main__':
    main()
