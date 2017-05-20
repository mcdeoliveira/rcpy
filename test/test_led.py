import pytest

import time
import rcpy.led as led

def test1():

    led.green.on()
    assert led.green.get_state() == led.ON
    
    led.green.off()
    assert led.green.get_state() == led.OFF
    
    led.red.on()
    assert led.red.get_state() == led.ON
    
    led.red.off()
    assert led.red.get_state() == led.OFF

if __name__ == '__main__':

    test1()
