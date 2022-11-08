from GreenPonik_PH import GreenPonik_PH
from machine import ADC
from time import sleep
import math


adc = ADC(26)
ph = GreenPonik_PH()
ph.begin()


while True:
    analog = adc.read_u16()
    PH = ph.readPH(analog)
    print("PH:%.2f " % (PH))