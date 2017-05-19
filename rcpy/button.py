import signal

from rcpy._buttons import pressed as _pressed
from rcpy._buttons import released as _released

# definitions

# BUTTONs
PAUSE  = 0
MODE = 1

# class for timeout
class TimeoutException(Exception):
    pass

# timeout handler
def timeout_handler(signum, frame):
    raise TimeoutException()

# pressed?
def pressed(button, timeout = 0):

    # set a timeout
    if timeout > 0:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

    try:
        return _pressed(button)
    except TimeoutException:
        return False

# released?
def released(button, timeout = 0):

    # set a timeout
    if timeout > 0:
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        
    try:
        return _released(button)
    except TimeoutException:
        return False
