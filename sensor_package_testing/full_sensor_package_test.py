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
    ph = PH(27)
    oled = Oled(0, 1)
    # temp, dev = temp_init(15)

    while True:
        tb_val = tb.get_turbidity()
        ph_val = ph.get_ph()
        print(ph_val)
        oled.clear()
        oled.show_oled("tb: ", tb_val, 0, 0)
        oled.show_oled("pH: ", ph_val, 0, 10)
        oled.show()
        sleep(1)
        # temp.convert_temp()
        # sleep(1)
        # celcius = temp.read_temp(dev)        
        # print(celcius, " Celcius\n")
        # sleep(1)
#     tb_val = tb.get_turbidity()
#     ph_val = ph.get_ph()
#     oled.clear()
#     oled.show_oled("tb: ", tb_val, 0, 0)
#     oled.show_oled("pH: ", ph_val, 0, 25)
#     oled.show()
#     sleep(3)


if __name__ == "__main__":
    main()