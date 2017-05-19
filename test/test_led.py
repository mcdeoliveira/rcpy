import pytest

import time
import rcpy.led as led

def test1():

    led.set(led.GREEN, led.ON)
    assert led.get(led.GREEN) == led.ON
    
    led.set(led.GREEN, led.OFF)
    assert led.get(led.GREEN) == led.OFF
    
    led.set(led.RED, led.ON)
    assert led.get(led.RED) == led.ON
    
    led.set(led.RED, led.OFF)
    assert led.get(led.RED) == led.OFF

if __name__ == '__main__':

    test1()
