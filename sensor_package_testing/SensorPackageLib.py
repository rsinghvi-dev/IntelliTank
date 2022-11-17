from machine import ADC, Pin, I2C
from ssd1306 import SSD1306_I2C
from onewire import OneWire
from ds18x20 import DS18X20
from time import sleep_ms
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


class Oled:
    def __init__(self, sda_pin: int, scl_pin: int):
        self.i2c = I2C(0,sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self.oled = SSD1306_I2C(128, 64, self.i2c)

    def clear(self):
        self.oled.fill(0)
    
    def show_scr(self):
        self.oled.show()

    def show_oled(self, text: str, reading: float, x: int, y: int):
        self.oled.text(text, x, y)
        self.oled.text(str(round(reading,2)), len(text)+50, y)

    def welcome_screen(self):
        self.oled.text("Welcome to", 23, 0)
        self.oled.text("IntelliTank!",15,10)
        self.oled.text("Press 1 to view",2, 40)
        self.oled.text("menu options",15,50)
    

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


class Temperature:
    def _init_(self, pin_no):
        ow = OneWire(Pin(pin_no))
        self.temp = DS18X20(ow)
        self.roms = self.temp.scan() #scanning for all temperature sensors connected to pico
    
    def get_temp(self, scale = "F"):
        try:
            self.temp.convert_temp()
            sleep_ms(750)
            celcius = self.temp.read_temp(self.roms[0])
            if scale == "C":
                return celcius
            else:
                return self.temp.fahrenheit(celcius)
        except:
            return 0


class PH:
    def __init__(self, pin_no):
        self.adc = ADC(pin_no)
        
    def get_ph(self):
        try:
            voltage = self.adc.read_u16()/16.004
            ph = float((-3*voltage)/653.0) + 15.6922
            return ph
        except:
            return 0