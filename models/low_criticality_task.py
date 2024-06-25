import configs
from . import BaseTask


class LowCriticalityTask(BaseTask):
    def __init__(self, computation_time: int, period: int):
        super(LowCriticalityTask, self).__init__(period, configs.CriticalityValues.LOW)
        self.computation_time = computation_time

    def get_deadline(self, mode: configs.Mode):
        return self.current_job * self.period + self.deadline

    def get_computation_time(self, mode: configs.Mode):
        return self.computation_time
