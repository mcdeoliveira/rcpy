from rc.rcpy import *

# make sure it is disabled when destroyed
import atexit; atexit.register(cleanup)

# constants
IDLE = 0
RUNNING = 1
PAUSED = 2
EXITING = 3
