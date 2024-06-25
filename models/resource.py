import configs


class Resource:
    def __init__(self, capacity):
        self.mutex = configs.Mutex.UNLOCK
        self.capacity = capacity

    def lock(self):
        self.mutex = configs.Mutex.LOCK

    def unlock(self):
        self.mutex = configs.Mutex.UNLOCK

    def is_locked(self):
        return self.mutex == configs.Mutex.LOCK
