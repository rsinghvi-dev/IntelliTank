from SensorPackageLib import Turbidity, Oled, PH
from ds18x20 import DS18X20
from machine import Pin
from onewire import OneWire
from time import sleep

# def temp_init(pin_no):
#     ow = OneWire(Pin(pin_no))
#     temp = DS18X20(ow)
#     roms = temp.scan() #scanning for all temperature sensors connected to
#     return temp, roms[0]



def main():
    tb = Turbidity(26)
    ph = PH(28)
    oled = Oled(0, 1)


    while True:

        info_request = input()
        if info_request == "":
            #this is pressing enter
            sensor = input("tb or ph?")
            if sensor == "tb":
                oled.clear()
                oled.show_oled("tb: ", tb.get_turbidity(), 0, 0)
                oled.show_scr()
            elif sensor == "ph":
                oled.clear()
                oled.show_oled("pH: ", ph.get_ph(), 0, 0)
                oled.show_scr()



if __name__ == "__main__":
    main()
    