import math
import time
from machine import ADC
from ds18x20 import DS18X20Single
from onewire import OneWire

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
        
        
class Temperature:
    
    def __init__(self, pin_no):
        self.ow = OneWire(machine.Pin(pin_no))
        self.temp = DS18X20Single(ow)
        self.roms = self.ds_sensor.scan() #scanning for all temperature sensors connected to pico
        self.temp.convert_temp()
    
    def get_temp(self, scale):
#     print("--------")
        try:
            celcius = self.temp.read_temp()
            if scale == "C":
                return celcius
            else:
                return self.temp.fahrenheit(celcius)
        except:
            return 0
        
        
class Turbidity:
    def __init__(self, pin_no):
        self.adc = ADC(pin_no)
        self.conversion_factor = 3.3 / (65535.0)
    
    def get_turbidity(self):
        try:
            analog = self.adc.read_u16()
            voltage = (analog*self.conversion_factor)+1.76
            if voltage <= 2.56:
                voltage = 2.56
            turbidity = (-1120.4*(voltage**2)) + (5742.3*voltage) - 4352.9
            return turbidity
        except:
            return 0