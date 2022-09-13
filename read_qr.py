import access
import cv2 as cv
import time

def main():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    READING_INTERVAL = 2
    start_reading_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        qrDetector = cv.QRCodeDetector()

        reading_time = time.time()
        elapsed_reading_time = reading_time - start_reading_time
        if elapsed_reading_time < READING_INTERVAL:
            continue

        data, _, _ = qrDetector.detectAndDecode(frame)
        if data:
            if not access.has_permission(data):
                print(f'{data} read')
            start_reading_time = time.time()
        cv.waitKey(5)

    cap.release()

if __name__ == '__main__':
    main()
