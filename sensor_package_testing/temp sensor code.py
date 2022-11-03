#make sure this is run with the Micropython (Raspberry Pi Pico) interpreter

import time, machine, onewire, ds18x20
#import adafruit_circuitpython_ds18x20
#from adafruit_ds18x20 import DS18X20

ds_pin = machine.Pin(17)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan() #scanning for all temperature sensors connected to pico

print('Found DS devices: ', roms)

while True:
#     print("--------")
    
    ds_sensor.convert_temp() #this is the temperature in celcius
    
    time.sleep_ms(750)
    
    for rom in roms:
        
        #print(rom)
        
        print(ds_sensor.read_temp(rom) * 1.8 + 32, "Fahrenheit") #in every iteration we are converting C to F
               
    time.sleep(2)