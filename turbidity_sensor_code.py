from machine import ADC
from time import sleep

adc = ADC(26)
conversion_factor = 3.3 / (65535)
initial_conversion_factor = (3.3 / 1024.0)

while True:
#     value = adc.read_u16()
    analog_value = adc.read_u16()
    digital_value = analog_valueconversion_factor
    print("Analog value is: " + str(analog_value))
#     print("Digital value (uv): " + str(value/1000000))

    voltage =  analog_value initial_conversion_factor # convert the analog read (which goes from 0-1023) to a voltage (0-5v)
#     turbidity = -1120.4(value**2) + 5742.3value - 4352.9
    print("Voltage value? is: " + str(voltage))

    sleep(1)