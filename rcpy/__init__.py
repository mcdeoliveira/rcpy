import warnings
import signal
from rcpy.rcpy import *

def handler(signum, frame):
    warnings.warn('Signal handler called with signal {}'.format(signum))
    # call cleanup functions 
    for fun, pars in cleanup_functions.items():
        fun(*pars)
        
    # call rcpy cleanup
    cleanup()
    
    # no need to cleanup later
    atexit.unregister(cleanup)

    warnings.warn('> Robotics cape exited cleanly')

    raise KeyboardInterrupt()
    
# make sure it is disabled when exiting cleanly
import atexit; atexit.register(cleanup)

# constants
IDLE = 0
RUNNING = 1
PAUSED = 2
EXITING = 3

# initialize cape
initialize()
set_state(PAUSED)
warnings.warn('> Robotics cape initialized')

# clean up handler
cleanup_functions = {}
def add_cleanup(fun, pars):
    cleanup_functions[fun] = pars

# install handler
warnings.warn('> Installing signal handlers')
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
