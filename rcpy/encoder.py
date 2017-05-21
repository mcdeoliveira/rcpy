import rcpy
from rcpy._encoder import *

class Encoder:

    def __init__(self, channel, count = None):

        self.channel = channel
        if count is not None:
            self.set(count)

    def get(self):
        return get(self.channel)

    def set(self, count):
        set(self.channel, count)

    def reset(self):
        set(self.channel, 0)
        
# define leds
encoder1 = Encoder(1)
encoder2 = Encoder(2)
encoder3 = Encoder(3)
encoder4 = Encoder(4)
