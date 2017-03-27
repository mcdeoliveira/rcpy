import pytest

import time
import rcpy

def test1():

    # initialize
    rcpy.initialize()
    assert rcpy.get_state() == rcpy.IDLE

    # clean up
    rcpy.cleanup()
    assert rcpy.get_state() == rcpy.EXITING

    # initialize again
    rcpy.initialize()
    assert rcpy.get_state() == rcpy.IDLE

    # set state
    rcpy.set_state(rcpy.PAUSED)
    assert rcpy.get_state() == rcpy.PAUSED

    # set state
    rcpy.set_state(rcpy.RUNNING)
    assert rcpy.get_state() == rcpy.RUNNING

if __name__ == '__main__':

    test1()
