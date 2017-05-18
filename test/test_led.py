import pytest

import time
import rcpy.LED as LED

def test1():

    LED.set(LED.GREEN, LED.ON)
    LED.set(LED.GREEN, LED.OFF)
    LED.set(LED.RED, LED.ON)
    LED.set(LED.RED, LED.OFF)

if __name__ == '__main__':

    test1()
