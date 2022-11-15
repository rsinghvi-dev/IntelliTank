from SensorPackageLib import Turbidity, Oled
from ds18x20 import DS18X20
from machine import Pin
from onewire import OneWire
from time import sleep

def temp_init(pin_no):
    ow = OneWire(Pin(pin_no))
    temp = DS18X20(ow)
    roms = temp.scan() #scanning for all temperature sensors connected to
    return temp, roms[0]


def main():
    # tb = Turbidity(26)
    # oled = Oled(0, 1)
    temp, dev = temp_init(15)

    while True:
        # turbidity = tb.get_turbidity()
        # oled.show_oled(turbidity)
        # sleep(3)
        temp.convert_temp()
    
        sleep(1)
        celcius = temp.read_temp(dev)        
        print(celcius, " Celcius\n")
        sleep(1)

if __name__ == "__main__":
    main()