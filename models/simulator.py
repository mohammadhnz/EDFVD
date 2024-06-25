import configs


class Simulator:
    def __init__(self):
        self.mode = configs.Mode.NORMAL
        self.queue = []