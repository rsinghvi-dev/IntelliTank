from machine import ADC
from time import sleep
import math
        
dummy = 0      
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

