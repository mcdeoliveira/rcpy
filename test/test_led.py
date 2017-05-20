import pytest

import time
import rcpy.gpio as gpio
import rcpy.led as led

def test1():

    led.green.on()
    assert led.green.is_on()
    assert led.green.pin.is_low()
    
    led.green.off()
    assert led.green.is_off()
    assert led.green.pin.is_high()
    
    led.red.on()
    assert led.red.get_state() == led.ON
    assert led.red.is_on()
    assert led.red.pin.is_low()
    
    led.red.off()
    assert led.red.is_off()
    assert led.red.pin.is_high()

if __name__ == '__main__':

    test1()
