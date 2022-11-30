from SensorPackageLib import Turbidity, PH, TDS
from ds18x20 import DS18X20
from machine import Pin, UART
from onewire import OneWire
from time import sleep, sleep_ms

def temp_init(pin_no):
    ow = OneWire(Pin(pin_no))
    temp = DS18X20(ow)
    print("---------")
    roms = temp.scan() #scanning for all temperature sensors connected to
    print("++++++++++++")
    return roms[0], temp
    

def get_temp(roms, temp):
    temp.convert_temp()
    sleep(0.75)
    reading = temp.read_temp(roms)
    return reading


def main():
    
    # ---Initialize devices---
    tb = Turbidity(26)
    ph = PH(28)
#     oled = Oled(0, 1)
    rom, temp = temp_init(22)
#     keypad = Keypad()
#     feeder = Feeder(10)
#     tds = TDS(27)
    oled_uart = UART(0, 9600, tx=Pin(16), rx=Pin(17))
    oled_uart.init(9600, bits=8, parity=None, stop=1)

    while True:
        buf = "%.1f,%.1f,%.1f\n\r" %(tb.get_turbidity(), ph.get_ph(), get_temp(rom, temp))
#         oled_uart.write(buf)
        print(buf)
#         key=keypad.keypad_read()
#         if key != None:
#             print("You pressed: "+key)
#             sleep(0.3)
#             if key == "A":
#                 oled.show_oled("tb: ", round(tb.get_turbidity(), 2), 0, 0)
#             if key == "B":
#                 oled.show_oled("pH: ", round(ph.get_ph(), 2), 0, 0)
#             if key == "C":
#                 oled.show_oled("temp: ", round(get_temp(rom, temp), 2), 0, 0)
#                 pass
#             if key == "D":
#                 oled.show_oled("tds: ", round(tds.get_tds(), 2), 0, 0)
#             if key == "*":
#                 feeder.feed()
        sleep(2)



if __name__ == "__main__":
    main()
    