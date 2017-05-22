import warnings
import signal
from rcpy.rcpy import initialize, cleanup
from rcpy.rcpy import set_state as _set_state

# constants
IDLE = 0
RUNNING = 1
PAUSED = 2
EXITING = 3

# create files for keeping track of state
_RC_DIR = '/tmp/robotics_cape'
_RC_STATE = _RC_DIR + '/state'
_RC_STATE_FD = open(_RC_STATE, 'bw+', buffering = 0)

# set state 
def set_state(state,  fd = _RC_STATE_FD):
    # call robotics cape set_state
    _set_state(state)
    # write to stream
    fd.seek(0)
    fd.write(state)

# idle function
def idle():
    set_state(IDLE)

# run function
def run():
    set_state(RUNNING)
    
# pause function
def pause():
    set_state(PAUSED)
    
# exit function
def exit():
    set_state(EXITING)

# cleanup handler
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

# initialize cape
initialize()

# set initial state
set_state(PAUSED)
warnings.warn('> Robotics cape initialized')

# setup clean up handler
cleanup_functions = {}
def add_cleanup(fun, pars):
    cleanup_functions[fun] = pars

# install handler
warnings.warn('> Installing signal handlers')
signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)
