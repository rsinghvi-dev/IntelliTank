from machine import Pin, ADC
from time import sleep
import math

adc_pin = Pin(26, mode=Pin.IN)
adc = ADC(adc_pin)
# adc = ADC(2)

while True:
    print(adc.read_u16())
#     voltage = adc.read_u16()*5.0/65535
#     PH = float((-3*voltage)/653.0) + 15.6922
#     print(voltage)
#     print("Voltage:%.4f " % (voltage))
#     print("PH:%.2f " % (PH))
    sleep(0.5)


