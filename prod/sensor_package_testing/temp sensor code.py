from time import sleep
from SensorPackageLib import Temperature

# while True:
#     tmp = Temperature(15)
#     tmp.convert()
#     sleep(1)
#     print("Temperature in C: " + str(tmp.get_temp("C")))
#     print("Temperature in F: " + str(tmp.get_temp("F")))

#make sure this is run with the Micropython (Raspberry Pi Pico) interpreter

import time, machine, onewire, ds18x20
#import adafruit_circuitpython_ds18x20
#from adafruit_ds18x20 import DS18X20

ds_pin = machine.Pin(15)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

dev = ds_sensor.scan() #scanning for all temperature sensors connected to pico

while True:
#     print("--------")
    ds_sensor.convert_temp()
    
    time.sleep_ms(750)
    
    print(ds_sensor.read_temp(dev[0]), "Fahrenheit") #in every iteration we are converting C to F
               
    time.sleep(2)