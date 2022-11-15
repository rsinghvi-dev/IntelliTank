import math
import sys
import time
from machine import ADC
 
class TDS:
 
    def __init__(self, channel):
        self.adc = ADC(channel)
 
    def get_tds(self):
        value = self.adc.read_u16()
        if value != 0:
            voltage = value* (3.3 / (65535.0))
            tdsValue = (133.42*voltage*voltage*voltage-255.86*voltage*voltage+857.39*voltage)*0.5
            return tdsValue
        else:
            return 0

def main():
    sensor = TDS(27)
    print('Detecting TDS...')
 
    while True:
        print('TDS Value: ' + str(sensor.get_tds()))
        time.sleep(1)
 
if __name__ == '__main__':
    main()
