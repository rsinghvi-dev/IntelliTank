from neopixel import Neopixel

numpix = 60
strip = Neopixel(numpix, 0, 1, "GRB")

hue = 0
while(True):
    color = strip.colorHSV(hue, 255, 150)
    strip.fill(color)
    strip.show()
    
    hue += 150