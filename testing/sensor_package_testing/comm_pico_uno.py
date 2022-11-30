from machine import UART
from time import sleep

oled_uart = UART(0, 9600)
oled_uart.init(9600, bits=8, parity=None, stop=1)

while True:
    buf = "Sach Jankharia is awesome!\n\0"
    oled_uart.write(buf)
    print("Done")
    sleep(1)
