import json

import configs


class BaseTask:
    def __init__(self, period: int, criticality: configs.CriticalityValues):
        self.period = period
        self.criticality = criticality
        self.deadline = None
        self.current_job = 0
        self.spent_calculation_time = 0

    def get_deadline(self, mode: configs.Mode):
        pass

    def get_computation_time(self, mode: configs.Mode):
        pass

    def calculate(self):
        self.spent_calculation_time += 1

    def advanced_forward_job(self):
        self.current_job += 1
        self.spent_calculation_time = 0

    def is_finished(self, mode: configs.Mode):
        if self.get_computation_time(mode) == self.spent_calculation_time:
            return True

    def is_active(self, current_time):
        if self.current_job * self.period >= current_time:
            return True

    def __repr__(self):
        return json.dumps(self.to_dict())