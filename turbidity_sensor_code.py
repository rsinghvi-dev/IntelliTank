# from machine import ADC
# from time import sleep

# adc = ADC(26)
# initial_conversion_factor = (3.3 / 1024.0)
# 
# while True:
#     
#     value = adc.read_u16()
#     analog_value = adc.read_u16()
#     digital_value = analog_value*conversion_factor
#     print("Analog value is: " + str(analog_value))
#     print("Digital value (uv): " + str(value/1000000))
# 
#     voltage = analog_value*initial_conversion_factor # convert the analog read (which goes from 0-1023) to a voltage (0-5v)
#     turbidity = -1120.4(value**2) + 5742.3value - 4352.9
#     print("Voltage value? is: " + str(voltage))
# 
#     sleep(1)

#### New Trial Code for Turbidity Sensor ####

from machine import ADC
from time import sleep
import math
        
        
adc = ADC(26)
conversion_factor = 3.3 / (65535.0)

while True:
    analog = adc.read_u16()
#     print("Analog Value is: ", analog)
    voltage = (analog*conversion_factor)+1.76
    
    if voltage <= 2.56:
        voltage = 2.56
    turbidity = (-1120.4*(voltage**2)) + (5742.3*voltage) - 4352.9
    print("Voltage is: " + str(round(voltage, 2)))
    print("Turbidity is: " + str(turbidity) +'\n')
    sleep(3)