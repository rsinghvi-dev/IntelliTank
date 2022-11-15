from machine import ADC, Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep
import math


class Turbidity:
    def __init__(self, pin_no):
        self.adc = ADC(pin_no)
        self.conversion_factor = 3.3 / (65535.0)
    
    def get_turbidity(self):
        analog = self.adc.read_u16()
        voltage = (analog*self.conversion_factor)+1.76
        if voltage <= 2.56:
            voltage = 2.56
        turbidity = (-1120.4*(voltage**2)) + (5742.3*voltage) - 4352.9
        # print("Voltage is: " + str(round(voltage, 2)))
        # print("Turbidity is: " + str(turbidity) +'\n')
        return turbidity


class Oled:
    def __init__(self, sda_pin: int, scl_pin: int):
        self.i2c = I2C(0,sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        self.oled = SSD1306_I2C(128, 64, self.i2c)

    def show_oled(self, reading):
        self.oled.fill(0)
        self.oled.text("ADC: ",5,8)
        self.oled.text(str(round(reading,2)),40,8)
        self.oled.show()
