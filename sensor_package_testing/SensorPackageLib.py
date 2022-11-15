from machine import ADC, Pin, I2C
from ssd1306 import SSD1306_I2C
import math


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
        # print("Voltage is: " + str(round(voltage, 2)))
        # print("Turbidity is: " + str(turbidity) +'\n')


class Oled:
    def __init__(self, sda_pin: int, scl_pin: int):
        self.i2c = I2C(0,sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self.oled = SSD1306_I2C(128, 64, self.i2c)

    def show_oled(self, reading):
        self.oled.fill(0)
        self.oled.text("ADC: ",5,8)
        self.oled.text(str(round(reading,2)),40,8)
        self.oled.show()


class TDS:
     
    def _init_(self, channel):
        self.adc = ADC(channel)
 
    def get_tds(self):
        value = self.adc.read_u16()
        if value != 0:
            voltage = value* (3.3 / (65535.0))
            tdsValue = (133.42*voltage*voltage*voltage-255.86*voltage*voltage+857.39*voltage)*0.5
            return tdsValue
        else:
            return 0


# Simpler to use in main code
# class Temperature:
#     
#     def _init_(self, pin_no):
#         ow = OneWire(Pin(pin_no))
#         self.temp = DS18X20Single(ow)
#         self.roms = self.temp.scan() #scanning for all temperature sensors connected to pico
#     
#     def get_temp(self, scale):
# #     print("--------")
#         try:
#             self.temp.convert_temp()
#             sleep_ms(750)
#             celcius = self.temp.read_temp(self.roms[0])
#             if scale == "C":
#                 return celcius
#             else:
#                 return self.temp.fahrenheit(celcius)
#         except:
#             return 0


# ***** To do *****

# class PH:
    
#     def _init_(self, pin_no, neutral, acid):
#         self.adc = ADC(pin_no)
#         self.neutral = neutral
#         self.acid = acid
        
#     def get_ph(self):
#         try:
#             voltage = self.adc.read_u16()/16.004
#             ph = float((-3*voltage)/653.0) + 15.6922
#             return ph
#         except:
#             return 0