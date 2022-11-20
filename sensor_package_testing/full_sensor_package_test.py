from SensorPackageLib import Turbidity, Oled, PH, Keypad
from ds18x20 import DS18X20
from machine import Pin
from onewire import OneWire
from time import sleep
import utime

# def temp_init(pin_no):
#     ow = OneWire(Pin(pin_no))
#     temp = DS18X20(ow)
#     roms = temp.scan() #scanning for all temperature sensors connected to
#     return temp, roms[0]



def main():
    tb = Turbidity(26)
    ph = PH(28)
    oled = Oled(0, 1)
    keypad = Keypad()

    while True:
        key=keypad.keypad_read()
        if key != None:
            print("You pressed: "+key)
            utime.sleep(0.3)
            if key == "A":
                oled.show_oled("tb: ", tb.get_turbidity(), 0, 0)
            if key == "B":
                oled.show_oled("pH: ", ph.get_ph(), 0, 0)
            if key == "C":
                oled.show_oled("temp: ", 69.69, 0, 0) 
            if key == "D":
                oled.show_oled("tds: ", 123.4, 0, 0)



if __name__ == "__main__":
    main()
    