import rcpy
from rcpy._servo import *
import rcpy.clock as clock

import threading, time

class Servo(clock.Action):

    def __init__(self, channel, duty = 0):
        self.channel = channel
        self.duty = duty

    def set(self, duty):
        self.duty = duty

    def pulse(self):
        servo.pulse(self.channel, self.duty)

    run = pulse
        
    def start(self, period):
        thread = Pulse([self], period)
        thread.start()
        return thread
        
# define servos
servo1 = Servo(1)
servo2 = Servo(2)
servo3 = Servo(3)
servo4 = Servo(4)
servo5 = Servo(5)
servo6 = Servo(6)
servo7 = Servo(7)
servo8 = Servo(8)
