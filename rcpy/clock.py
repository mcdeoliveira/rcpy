import rcpy

import threading, time, warnings

class Action:
    
    def run(self):
        raise Exception("Method run has not been defined yet.")

class Actions(Action):

    def __init__(self, *actions):
        self.actions = actions

    def run(self):
        for a in self.actions:
            a.run()
    
class Clock(threading.Thread):

    def __init__(self, action, period = 1):

        # call super
        super().__init__()
        
        self.condition = threading.Condition()
        self.period = period

        if isinstance(action, Action):
            self.action = action
        else:
            raise Exception("action must be of class Action")
        
        self._suspend = False

    def set_period(self, period):
        self.period = period

    def toggle(self):
        self._suspend = not self._suspend

    def _run(self):

        # Acquire lock
        self.condition.acquire()

        # Toggle
        if not self._suspend:
            self.action.run()
        
        # Notify lock
        self.condition.notify_all()

        # Release lock
        self.condition.release()
    
    def run(self):

        self.run = True
        while rcpy.get_state() != rcpy.EXITING and self.run:

            # Acquire condition
            self.condition.acquire()
            
            # Setup timer
            self.timer = threading.Timer(self.period, self._run)
            self.timer.start()

            # Wait 
            self.condition.wait()

            # and release
            self.condition.release()

    def stop(self):

        self.run = False;
        
        # Acquire lock
        self.condition.acquire()

        # Notify lock
        self.condition.notify_all()

        # Release lock
        self.condition.release()
