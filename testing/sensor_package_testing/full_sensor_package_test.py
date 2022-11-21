from SensorPackageLib import Turbidity, Oled, PH, Keypad, Feeder, Temperature, TDS
from ds18x20 import DS18X20
from machine import Pin
from onewire import OneWire
from time import sleep
import utime

def temp_init(pin_no):
    ow = OneWire(Pin(pin_no))
    temp = DS18X20(ow)
    print("---------")
    roms = temp.scan() #scanning for all temperature sensors connected to
    print("++++++++++++")
    return roms[0], temp
    

def get_temp(roms, temp):
    temp.convert_temp()
    sleep(1)
    reading = temp.read_temp(roms)
    sleep(2)
    return reading


def main():
    tb = Turbidity(26)
    ph = PH(28)
    oled = Oled(0, 1)
#     temp = Temperature(11)
    roms, temp = temp_init(15)
    keypad = Keypad()
    feeder = Feeder(10)
    tds = TDS(27)

    while True:
        key=keypad.keypad_read()
        if key != None:
            print("You pressed: "+key)
            utime.sleep(0.3)
            if key == "A":
                oled.show_oled("tb: ", round(tb.get_turbidity(), 2), 0, 0)
            if key == "B":
                oled.show_oled("pH: ", round(ph.get_ph(), 2), 0, 0)
            if key == "C":
                oled.show_oled("temp: ", round(get_temp(roms, temp), 2), 0, 0)
                pass
            if key == "D":
                oled.show_oled("tds: ", round(tds.get_tds(), 2), 0, 0)
            if key == "*":
                feeder.feed()



if __name__ == "__main__":
    main()
    