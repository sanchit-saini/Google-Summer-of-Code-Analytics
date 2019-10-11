class LogHelper:

    def __init__(self, **kwds):
        self.debug = kwds['debug']

    def errorLog(self, msg):
        print(msg)
        exit(1)

    def debugLog(self, msg):
        if self.debug:
            print(msg)

    def log(self, msg):
        print(msg)
        exit(0)
