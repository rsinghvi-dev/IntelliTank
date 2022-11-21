from machine import ADC
from time import sleep
import math


adc = ADC(26)


while True:
    voltage = adc.read_u16()/16.004
    PH = float((-3*voltage)/653.0) + 15.6922
    print("Voltage:%.4f " % (voltage))
    print("PH:%.2f " % (PH))
    sleep(1)


