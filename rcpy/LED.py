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

class blinkThread(threading.Thread):
    
    def __init__(self, led, hz):
        self.led = led
        self.T = 1/hz
        self.state = OFF
    
    def run(self):
        while True:
            set(led, self.state)
            self.state = not self.state
            time.sleep(self.T)

def blink(led, hz, period):

    if period > 0:
        _blink(led, hz, period)
    
    elif period <= 0:
        thread = blinkThread(led, hz)
        thread.start()
        return thread
