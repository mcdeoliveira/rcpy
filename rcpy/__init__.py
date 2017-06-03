import warnings
import signal
import os, time

from rcpy._rcpy import initialize, cleanup, get_state
from rcpy._rcpy import set_state as _set_state
from rcpy._rcpy import cleanup as _cleanup

#from hanging_threads import start_monitoring
#monitoring_thread = start_monitoring()

# constants
IDLE = 0
RUNNING = 1
PAUSED = 2
EXITING = 3

# create pipes for communicating state
_RC_STATE_PIPE_LIST = []

def _get_state_pipe_list(p = _RC_STATE_PIPE_LIST):
    return p

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
    # write to open pipes
    for (r_fd, w_fd) in _get_state_pipe_list():
        os.write(w_fd, bytes(str(state), 'UTF-8'))
    # call robotics cape set_state
    _set_state(state)

# cleanup function
_CLEANUP_FLAG = False
def cleanup():
    global _CLEANUP_FLAG
    # return to avoid multiple calls to cleanup
    if _CLEANUP_FLAG:
        return
    _CLEANUP_FLAG = True

    print('Initiating cleanup...')
    # get state pipes
    pipes = _get_state_pipe_list()
    if len(pipes):
        print('{} pipes open'.format(len(pipes)))

    # set state as exiting
    set_state(EXITING)
        
    print('Calling roboticscape cleanup')
    # call robotics cape cleanup
    _cleanup()

    if len(pipes):
        print('Closing pipes')
        # close open pipes left
        while len(pipes):
            destroy_pipe(pipes[0])
        
    print('Dnoe with cleanup')
    
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
