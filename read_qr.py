import access
import cv2 as cv
import logging
import time
import sys

def handle_unhandled_exceptions(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.critical('Unhandled exception', exc_info=(exc_type, exc_value, exc_traceback))
    logging.info('END')

def main():
    now   = time.localtime()
    year  = now.tm_year
    month = now.tm_mon
    day   = now.tm_mday

    logging.basicConfig(filename=f'logs/{year}_{month}_{day}_access.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - [%(levelname)s] %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S')

    sys.excepthook = handle_unhandled_exceptions

    logging.info('START')
    
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
