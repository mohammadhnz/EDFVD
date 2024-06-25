import configs


class Resource:
    def __init__(self):
        self.mutex = configs.Mutex.UNLOCK

    def lock(self):
        self.mutex = configs.Mutex.LOCK

    def unlock(self):
        self.mutex = configs.Mutex.UNLOCK
