import rcpy
from rcpy._servo import *

import threading, time

class Pulse(threading.Thread):

    def __init__(self, servos, period):

        super().__init__()
        
        self.condition = threading.Condition()
        if isinstance(servos, Servo):
            self.servos = [servos]
        elif isinstance(servos, (list, tuple)):
            self.servos = servos
        else:
            raise Exception("servos must be a Servo or lists of Servo objects")
        self.period = period
        self._suspend = False

    def set_period(self, period):
        self.period = period

    def toggle(self):
        self._suspend = not self._suspend
        
    def _pulse(self):

        # Acquire lock
        self.condition.acquire()

        # Pulse
        if not self._suspend:
            for s in self.servos:
                s.pulse()
        
        # Notify lock
        self.condition.notify_all()

        # Release lock
        self.condition.release()
    
    def run(self):

        self.run = True
        while rcpy.get_state() != rcpy.EXITING and self.run:

            # Acquire condition
            self.condition.acquire()
            
            # Setup timer
            self.timer = threading.Timer(self.period, self._pulse)
            self.timer.start()

            # Wait 
            self.condition.wait()

            # and release
            self.condition.release()

    def stop(self):

        self.run = False;
        
        # Acquire lock
        self.condition.acquire()

        # Notify lock
        self.condition.notify_all()

        # Release lock
        self.condition.release()

class Servo:

    def __init__(self, channel, duty = None):
        self.channel = channel
        if duty is not None:
            self.set(duty)

    def set(self, duty):
        self.duty = duty

    def pulse(self):
        pulse(self.channel, self.duty)

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
