import serial

def main():
    pass

def prohibited():
    with serial.Serial('/dev/ttyACM0') as ser:
        ser.write(b'a')

def release():
    with serial.Serial('/dev/ttyACM0') as ser:
        ser.write(b'q')

if __name__ == "__main__":
    main()
