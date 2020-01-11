import time


class Timing:
    def __init__(self):
        self.start = time.time()
        self.result = None

    def end(self):
        self.result = time.time() - self.start

    def log(self):
        print('-'*60)
        print('Execution time was ended after %.3f seconds.' %(self.result))
        print('-'*60)
