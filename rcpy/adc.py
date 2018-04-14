import rcpy
from rcpy._adc import *

CHANNEL_COUNT   = 7
CHANNEL_MIN     = 0
CHANNEL_MAX     = 6

class ADC:

    def __init__(self, channel):
        self.channel = channel

    def get_raw(self):
        return get_raw(self.channel)

    def get_voltage(self):
        return get_voltage(self.channel)

class DC_Jack:

    def get_voltage(self):
        return get_dc_jack_voltage()

class Battery:

    def get_voltage(self):
        return get_battery_voltage()

# define adcs
adc0 = ADC(0)
adc1 = ADC(1)
adc2 = ADC(2)
adc3 = ADC(3)
adc4 = ADC(4)
adc5 = ADC(5)
adc6 = ADC(6)

# list of ADCs, indexed by channel number
adc = [ adc0, adc1, adc2, adc3, adc4, adc5, adc6 ]

dc_jack = DC_Jack()

battery = Battery()

