from threading import Timer
class RepeatTimerThread(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
    def pause(self):
        self.cancel()
    def restart(self):
        self.run()