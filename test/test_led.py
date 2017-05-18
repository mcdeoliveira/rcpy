import pytest

import time
import rcpy.LED as LED

def test1():

    LED.led_set(LED.GREEN, LED.ON)
    LED.led_set(LED.GREEN, LED.OFF)
    LED.led_set(LED.RED, LED.ON)
    LED.led_set(LED.RED, LED.OFF)

if __name__ == '__main__':

    test1()
