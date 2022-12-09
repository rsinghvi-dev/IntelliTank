# 
# class Feeder:
#     def __init__(self, pin_no):
#         self.pwm = PWM(Pin(pin_no))
#         self.pwm.freq(50)
#         self.status = True
# 
#     def feed(self):
#         for position in range(0, 600, 50):
#             self.pwm.duty_u16(position)
#             sleep(.1)
#         self.pwm.duty_u16(0)
#         
# feeder = Feeder(0)
# feeder.feed()


# from time import sleep
# from machine import Pin, PWM
# 
# pwm = PWM(Pin(0))
# pwm.freq(50)



# for position in range(1000,9000,50):
#     pwm.duty_u16(position)
#     sleep(0.1)
# for position in range(9000,1000,-50):
#     pwm.duty_u16(position)
#     sleep(0.01)
# pwm.duty_u16(600)

from machine import Pin, PWM
import utime

MID = 1500000
#MIN = 1000000
MAX = 2000000

count = 0

# led = Pin(25,Pin.OUT)
pwm = PWM(Pin(15))

pwm.freq(50)
pwm.duty_ns(MID)

for i in range(5):
#     pwm.duty_ns(MIN)
#     utime.sleep(1)
    
    pwm.duty_ns(MID)
    utime.sleep(1)
    pwm.duty_ns(MAX)
    utime.sleep(1)
    count += 1
    print(count)
    if i == 1 or count == 1:
        pwm.duty_ns(0)      
        break
    
# for position in range(MID,MAX,50):
#     pwm.duty_u16(position)
#     sleep(0.01)
#     count += 1
#     print(count)
# pwm.duty_u16(600)