import configs
from . import BaseTask


class LowCriticalityTask(BaseTask):
    def __init__(self, computation_time: int, period: int):
        super().__init__(period, configs.CriticalityValues.LOW)
        self.computation_time = computation_time

