import warnings
import signal
import os, time

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

_RC_STATE_PIPE_LIST = []

# state functions
def _get_state_fd(fd = _RC_STATE_FD):
    return fd

def _get_state_pipe_list(p = _RC_STATE_PIPE_LIST):
    return p

def get_state_filename(filename = _RC_STATE):
    return filename

# creates pipes for communication

def create_pipe():
    r_fd, w_fd = os.pipe()
    _get_state_pipe_list().append((r_fd, w_fd))
    return (r_fd, w_fd)

def destroy_pipe(pipe):
    _get_state_pipe_list().remove(pipe)
    (r_fd, w_fd) = pipe
    os.close(r_fd)
    os.close(w_fd)

# set state 
def set_state(state):
    # get state fd
    fd = _get_state_fd()
    # call robotics cape set_state
    _set_state(state)
    # write to stream
    fd.seek(0)
    fd.write(bytes(str(state) + '\n', 'UTF-8'))
    # write to open pipes
    for (r_fd, w_fd) in _get_state_pipe_list():
        os.write(w_fd, bytes(str(state), 'UTF-8'))

# cleanup function
_CLEANUP_FLAG = False
def cleanup():
    global _CLEANUP_FLAG
    # return to avoid multiple calls to cleanup
    if _CLEANUP_FLAG:
        return
    _CLEANUP_FLAG = True
    
    print('> Start cleanup')
    # get state fd
    fd = _get_state_fd()
    pipes = _get_state_pipe_list()
    # call exit
    print('> will call exit')
    exit()
    time.sleep(.5)
    print('> any pipes? {}'.format(len(pipes)))
    # call robotics cape cleanup
    _cleanup()
    # closed streams
    fd.close()
    # close open pipes
    print('> any pipes? {}'.format(len(pipes)))
    while len(pipes):
        destroy_pipe(pipes[-1])
    
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
