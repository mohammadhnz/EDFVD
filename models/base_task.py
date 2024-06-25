import configs


class BaseTask:
    def __init__(self, period: int, criticality: configs.CriticalityValues):
        self.period = period
        self.criticality = criticality
