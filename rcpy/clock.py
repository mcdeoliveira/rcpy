import threading, time

class Clock(threading.Thread):

    def __init__(self, period = 1):

        super().__init__()
        
        self.condition = threading.Condition()
        self.period = period
        self._suspend = False

    def set_period(self, period):
        self.period = period

    def toggle(self):
        self._suspend = not self._suspend

    def action(self):
        raise Exception("Action has not been defined yet.")
        
    def _run(self):

        # Acquire lock
        self.condition.acquire()

        # Toggle
        if not self._suspend:
            self.action()
        
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
