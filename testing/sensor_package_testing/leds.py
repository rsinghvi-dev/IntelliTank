import machine
from time import sleep


led = machine.Pin("LED", machine.Pin.OUT)
while True:
    led.off()
    sleep(1)
    led.on()
    sleep(1)