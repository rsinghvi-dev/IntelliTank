from SensorPackageLib import Turbidity, PH
from ds18x20 import DS18X20
from machine import Pin, UART, ADC, PWM
from onewire import OneWire
from time import sleep, sleep_ms
import neopixel
import random
import _thread
# from qwiic_button import QwiicButton

MID = 1500000
#MIN = 1000000
MAX = 2000000 

def feeder_init(pin):
    pwm = PWM(Pin(pin))
    pwm.freq(50)
    pwm.duty_ns(MID)
    return pwm

def feed(pwm):
    pwm.duty_ns(MAX)
    sleep(1)
    pwm.duty_ns(MID)
    sleep(1)
    pwm.duty_ns(0)      

def temp_init(pin_no):
    ow = OneWire(Pin(pin_no))
    temp = DS18X20(ow)
    print("---------")
    roms = temp.scan() #scanning for all temperature sensors connected to
    print(roms)
    return roms[0], temp
    

def get_temp(roms, temp):
    temp.convert_temp()
    sleep_ms(750)
    reading = temp.read_temp(roms)
    return reading * 1.8 + 32 if reading is not None else None

def get_tds(adc):
    value = adc.read_u16() 
    voltage = value* (3.3 / (65535.0))
    tdsValue = (133.42*voltage*voltage*voltage-255.86*voltage*voltage+857.39*voltage)*0.5
    return tdsValue
    
def keypad_init(pin1, pin2, pin3, pin4):
    arr = [pin1, pin2, pin3, pin4]
    pins = [Pin(pin_no, Pin.IN, Pin.PULL_UP) for pin_no in arr]
    return pins

def second_thread():
    feeder = feeder_init(15)
    numpix = 60
    strip = neopixel.Neopixel(numpix, 1, 1, "GRBW")
    keys = keypad_init(3, 4, 5, 6)
    button_3 = keys[0]
    button_2 = keys[3]
    button_4 = keys[1]
    button_1 = keys[2]
    
    while True:
        if not button_4.value():
            feed(feeder)
        if not button_3.value():
            red = (255, 0, 0)
            orange = (255, 50, 0)
            yellow = (255, 100, 0)
            green = (0, 255, 0)
            blue = (0, 0, 255)
            indigo = (100, 0, 90)
            violet = (200, 0, 100)
            colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

            # same colors as normaln rgb, just 0 added at the end
            colors_rgbw = [color+tuple([0]) for color in colors_rgb]
            colors_rgbw.append((0, 0, 0, 255))

            # uncomment colors_rgbw if you have RGBW strip
            colors = colors_rgb
            # colors = colors_rgbw


            step = round(numpix / len(colors))
            current_pixel = 0
            strip.brightness(50)

            for color1, color2 in zip(colors, colors[1:]):
                strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
                current_pixel += step

            strip.set_pixel_line_gradient(current_pixel, numpix - 1, violet, red)

            while True:
                strip.rotate_right(1)
                sleep_ms(42)
                strip.show()
                if not button_1.value() or not button_2.value() or not button_4.value():
                    break
                    
        if not button_1.value():
            red = (255, 0, 0)
            orange = (255, 165, 0)
            yellow = (255, 150, 0)
            green = (0, 255, 0)
            blue = (0, 0, 255)
            indigo = (75, 0, 130)
            violet = (138, 43, 226)
            colors_rgb = (red, orange, yellow, green, blue, indigo, violet)

            # same colors as normaln rgb, just 0 added at the end
            colors_rgbw = [color+tuple([0]) for color in colors_rgb]
            colors_rgbw.append((0, 0, 0, 255))

            # uncomment colors_rgb if you have RGB strip
            # colors = colors_rgb
            colors = colors_rgbw

            strip.brightness(42)

            while True:
                for color in colors:
                    for i in range(numpix):
                        strip.set_pixel(i, color)
                        sleep_ms(10)
                        strip.show()
                        if not button_2.value() or not button_3.value() or not button_4.value():
                            break
                    if not button_2.value() or not button_3.value() or not button_4.value():
                        break    
                if not button_2.value() or not button_3.value() or not button_4.value():
                    break                        
                
        if not button_2.value():
            colors_rgb = [
                (232, 100, 255),  # Purple
                (200, 200, 20),  # Yellow
                (30, 200, 200),  # Blue
                (150,50,10),
                (50,200,10),
            ]

            # same colors as normaln rgb, just 0 added at the end
            colors_rgbw = [color+tuple([0]) for color in colors_rgb]
            colors_rgbw.append((0, 0, 0, 255))

            # uncomment colors_rgbw if you have RGBW strip
            colors = colors_rgb
            # colors = colors_rgbw

            max_len=20
            min_len = 5
            #pixelnum, posn in flash, flash_len, direction
            flashing = []

            num_flashes = 10

            for i in range(num_flashes):
                pix = random.randint(0, numpix - 1)
                col = random.randint(1, len(colors) - 1)
                flash_len = random.randint(min_len, max_len)
                flashing.append([pix, colors[col], flash_len, 0, 1])
                
            strip.fill((0,0,0))

            while True:
                strip.show()
                for i in range(num_flashes):

                    pix = flashing[i][0]
                    brightness = (flashing[i][3]/flashing[i][2])
                    colr = (int(flashing[i][1][0]*brightness), 
                            int(flashing[i][1][1]*brightness), 
                            int(flashing[i][1][2]*brightness))
                    strip.set_pixel(pix, colr)

                    if flashing[i][2] == flashing[i][3]:
                        flashing[i][4] = -1
                    if flashing[i][3] == 0 and flashing[i][4] == -1:
                        pix = random.randint(0, numpix - 1)
                        col = random.randint(0, len(colors) - 1)
                        flash_len = random.randint(min_len, max_len)
                        flashing[i] = [pix, colors[col], flash_len, 0, 1]
                    flashing[i][3] = flashing[i][3] + flashing[i][4]
                    sleep_ms(5)
                    if not button_1.value() or not button_3.value() or not button_4.value():
                        break
                    
                if not button_1.value() or not button_3.value() or not button_4.value():
                    break

            
    # ---Initialize devices---
tb = Turbidity(26)
ph = PH(28)
#     oled = Oled(0, 1)
rom, temp = temp_init(22)
#     keypad = Keypad()
tds = ADC(27)
heat_relay = Pin(2, Pin.OUT)
# feed_button = QwiicButton()
pi_uart = UART(0, 9600, tx=Pin(12), rx=Pin(13))
pi_uart.init(9600, bits=8, parity=None, stop=1)

_thread.start_new_thread(second_thread, ())

while True:
    tmp = get_temp(rom, temp)
#         heat_relay.value(1)
#     else:
#         heat_relay.value(0)

    ntu = tb.get_turbidity()
    ph_val = ph.get_ph()
    ppm = get_tds(tds)
    buf = "%.1f,%.1f,%.1f,%.1f,8.3\n" %(ntu, ph_val, tmp, ppm)
    pi_uart.write(buf)
    print(buf)
    # key=keypad.keypad_read()
    # if key != None:
    #     print("You pressed: "+key)
    #     sleep(0.3)
    #     if key == "A":
    #         oled.show_oled("tb: ", round(tb.get_turbidity(), 2), 0, 0)
    #     if key == "B":
    #         oled.show_oled("pH: ", round(ph.get_ph(), 2), 0, 0)
    #     if key == "C":
    #         oled.show_oled("temp: ", round(get_temp(rom, temp), 2), 0, 0)
    #         pass
    #     if key == "D":
    #         oled.show_oled("tds: ", round(tds.get_tds(), 2), 0, 0)
    #     if key == "*":
    #         feeder.feed()
    sleep(0.75)

