from machine import ADC
from time import sleep
import math
from turbidity import Turbidity

tb = Turbidity(26)

while True:
    tb.get_turbidity()
    sleep(3)


