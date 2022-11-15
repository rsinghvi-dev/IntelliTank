from SensorPackageLib import Turbidity, Oled
from time import sleep


tb = Turbidity(26)
oled = Oled(0, 1)

while True:
    turbidity = tb.get_turbidity()
    oled.show_oled(turbidity)
    sleep(3)

