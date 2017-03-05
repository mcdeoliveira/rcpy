import pytest

import time
import rc

def test1():

    # initialize
    rc.initialize()
    assert rc.get_state() == rc.IDLE

    # clean up
    rc.cleanup()
    assert rc.get_state() == rc.EXITING

    # initialize again
    rc.initialize()
    assert rc.get_state() == rc.IDLE

    # set state
    rc.set_state(rc.PAUSED)
    assert rc.get_state() == rc.PAUSED

    # set state
    rc.set_state(rc.RUNNING)
    assert rc.get_state() == rc.RUNNING

if __name__ == '__main__':

    test1()
