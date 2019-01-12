import seamonsters as sea

class Action:

    def __init__(self, name, generator):
        self.name = name
        self.generator = generator

class AutoScheduler:

    def __init__(self):
        self.actionList = []
        self.runningAction = None
        self.paused = False
        self._actionCancelled = False

    def updateGenerator(self):
        while True:
            if len(self.actionList) != 0 and not self.paused:
                self.runningAction = self.actionList.pop(0)
                yield from sea.watch(self.runningAction.generator, self._watchForCancelGenerator())
                self.runningAction = None
            else:
                yield

    def cancelRunningAction(self):
        self._actionCancelled = True

    def _watchForCancelGenerator(self):
        while not self._actionCancelled:
            yield
        self._actionCancelled = False
