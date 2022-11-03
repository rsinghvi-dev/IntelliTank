# import machine
# import time
# 
# led = machine.Pin('LED', machine.Pin.OUT)
# 
# while True:
#     
#     time.sleep(2)
    
from machine import Pin
led = Pin(25, Pin.OUT)

led.toggle()