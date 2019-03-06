class Action:

    def run(self):
        raise Exception("Method run has not been defined yet.")


class Actions(Action):

    def __init__(self, *actions):
        self.actions = actions

    def run(self):
        for a in self.actions:
            a.run()