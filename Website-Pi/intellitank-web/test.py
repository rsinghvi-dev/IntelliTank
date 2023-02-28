import serial
import time

ser = serial.Serial('/dev/ttyS0',
                    baudrate=9600,
					parity=serial.PARITY_NONE,
					stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)# Update with your serial port and baud rate

while True:
    try:
        data = ser.readline().decode('utf-8').rstrip()
        print(data)
    except:
        print('Error reading data from serial port')