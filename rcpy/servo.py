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

    def pulse(self, duty):
        self.duty = duty
        pulse(self.channel, self.duty)

    def run(self):
        pulse(self.channel, self.duty)
        
    def start(self, period):
        thread = clock.Clock(self, period)
        thread.start()
        return thread

class ESC(Servo):

    def pulse(self, duty):
        self.duty = duty
        esc_pulse(self.channel, self.duty)

    def run(self):
        esc_pulse(self.channel, self.duty)
    
# define servos
servo1 = Servo(1)
servo2 = Servo(2)
servo3 = Servo(3)
servo4 = Servo(4)
servo5 = Servo(5)
servo6 = Servo(6)
servo7 = Servo(7)
servo8 = Servo(8)

# define escs
esc1 = ESC(1)
esc2 = ESC(2)
esc3 = ESC(3)
esc4 = ESC(4)
esc5 = ESC(5)
esc6 = ESC(6)
esc7 = ESC(7)
esc8 = ESC(8)
