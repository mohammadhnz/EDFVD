import configs


class BaseTask:
    def __init__(self, period: int, criticality: configs.CriticalityValues):
        self.period = period
        self.criticality = criticality
        self.deadline = period

    def get_deadline(self, mode: configs.Mode):
        pass

    def get_computation_time(self, mode: configs.Mode):
        pass
