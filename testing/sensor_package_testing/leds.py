import time
from neopixel import Neopixel
import random


class TankLEDs:
    def __init__(self, pin, num_pixels):
        self.strip = Neopixel(num_pixels, 0, pin, "GRB")
        self.numpix = num_pixels
    
    def color_wave(self):
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


        step = round(self.numpix / len(colors))
        current_pixel = 0
        self.strip.brightness(50)

        for color1, color2 in zip(colors, colors[1:]):
            self.strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
            current_pixel += step

        self.strip.set_pixel_line_gradient(current_pixel, self.numpix - 1, violet, red)

        while True:
            self.strip.rotate_right(1)
            time.sleep(0.042)
            self.strip.show()
            
    def fireflies(self):
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
            pix = random.randint(0, self.numpix - 1)
            col = random.randint(1, len(colors) - 1)
            flash_len = random.randint(min_len, max_len)
            flashing.append([pix, colors[col], flash_len, 0, 1])
            
        self.strip.fill((0,0,0))

        while True:
            self.strip.show()
            for i in range(num_flashes):

                pix = flashing[i][0]
                brightness = (flashing[i][3]/flashing[i][2])
                colr = (int(flashing[i][1][0]*brightness), 
                        int(flashing[i][1][1]*brightness), 
                        int(flashing[i][1][2]*brightness))
                self.strip.set_pixel(pix, colr)

                if flashing[i][2] == flashing[i][3]:
                    flashing[i][4] = -1
                if flashing[i][3] == 0 and flashing[i][4] == -1:
                    pix = random.randint(0, self.numpix - 1)
                    col = random.randint(0, len(colors) - 1)
                    flash_len = random.randint(min_len, max_len)
                    flashing[i] = [pix, colors[col], flash_len, 0, 1]
                flashing[i][3] = flashing[i][3] + flashing[i][4]
                time.sleep(0.005)
                
    def rainbow(self):
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

        self.strip.brightness(42)

        while True:
            for color in colors:
                for i in range(numpix):
                    self.strip.set_pixel(i, color)
                    time.sleep(0.01)
                    self.strip.show()
                    
    def set_range(self, K):
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)

        # set the first K to red, next K to green, next K to blue;
        # and the rest to R,G,B,R,B  ... and then spin it.

        # reduce K, if numpix is < K*3+1
        K = min(K,(numpix-1)//3)

        strip.brightness(80)

        strip[:] = blue   # all to blue first...
        # now fill in the red & green...
        strip[:K] = red
        strip[K:2*K] = green
        strip[3*K::3] = red
        strip[3*K+1::3] = green

        self.strip.show()

        # show it for 5 seconds...
        time.sleep(5.0)

        # spin it...

        while(True):
            strip.rotate_right()
            strip.show()
            time.sleep_ms(500)
