from rcpy.led import set, get
from rcpy.led import blink as _blink

import threading
import time

# definitions

# LEDs
GREEN  = 0
RED = 1

# state
ON  = 1
OFF = 0

class __blink(threading.Thread):

    def __init__(self, led, hz):

        # call super
        super().__init__()
        
        self.state = ON
        self.led = led
        self.T = 1/hz
        
    def run(self):
        self.run = True
        while self.run:
            set(led, state)
            state = not state
            time.sleep(1/hz)

    def stop(self):
        self.run = False

def blink(led, hz, period):

    if period > 0:
        _blink(led, hz, period)
    
    elif period <= 0:
        thread = __blink(led, hz)
        thread.start()
        return thread
