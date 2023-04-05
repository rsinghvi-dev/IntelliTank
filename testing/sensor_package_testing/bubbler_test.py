from machine import Pin, ADC
from time import sleep
import math

bubbler_relay = Pin(0, Pin.OUT)



while True:
    print("bubbler on?")
    bubbler_relay.value(1)
    sleep(10)
    print("bubbler off?")
    bubbler_relay.value(0)
    sleep(5)