import warnings
import signal
import os

from rcpy.rcpy import initialize, cleanup, get_state
from rcpy.rcpy import set_state as _set_state
from rcpy.rcpy import cleanup as _cleanup

# constants
IDLE = 0
RUNNING = 1
PAUSED = 2
EXITING = 3

# create files for keeping track of state
_RC_DIR = '/tmp/robotics_cape'
_RC_STATE = _RC_DIR + '/state'
if not os.path.exists(_RC_DIR):
    os.makedirs(_RC_DIR)
_RC_STATE_FD = open(_RC_STATE, 'bw+', buffering = 0)

# state functions
def _get_state_fd(fd = _RC_STATE_FD):
    return fd

def get_state_filename(filename = _RC_STATE):
    return filename

# set state 
def set_state(state):
    # get state fd
    fd = _get_state_fd()
    # call robotics cape set_state
    _set_state(state)
    # write to stream
    fd.write(bytes(str(state) + '\n', 'UTF-8'))

# cleanup function
def cleanup():
    # get state fd
    fd = _get_state_fd()
    # call exit
    exit()
    # call robotics cape cleanup
    _cleanup()
    # closed stream
    fd.close()
    
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
