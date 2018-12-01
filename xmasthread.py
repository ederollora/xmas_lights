import threading

class ChristmasLightThread(threading.Thread):
    def __init__(self, name, function):
        super(ChristmasLightThread, self).__init__()
        self.paused = True
        self.state = threading.Condition()
        self.function = function
        self.name = name

    def start(self):
        super(ChristmasLightThread, self).start()

    def run(self):
        # self.resume() #unpause self
        while True:
            with self.state:
                if self.paused:
                    self.state.wait() #block until notifed
            while not self.paused:
                # Call function
                self.function()

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        with self.state:
            self.paused = Truex

    def __repr__(self):
        return "ChristmasLightThread()"

    def __str__(self):
        return "Thread: "+self.state+" , Paused: "+seld.state
