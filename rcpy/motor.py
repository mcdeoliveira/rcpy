import rcpy
from rcpy._motor import *

class Motor:

    def __init__(self, channel, duty = None):
        self.channel = channel
        if duty is not None:
            self.set(duty)

    def set(self, duty):
        set(self.channel, duty)

    def free_spin(self):
        set_free_spin(self.channel)

    def brake(self):
        set_brake(self.channel)
        
# define leds
motor1 = Motor(1)
motor2 = Motor(2)
motor3 = Motor(3)
motor4 = Motor(4)
