import math
from typing import List

import configs
from models import HighCriticalityTask, LowCriticalityTask


class Simulator:
    def __init__(self):
        self.mode = configs.Mode.NORMAL
        self.high_criticality_queue: List[HighCriticalityTask] = []
        self.low_criticality_queue: List[LowCriticalityTask] = []
        self.current_time = 0
        self.edf_vd_x = self._get_edf_vd_x()
        self._update_high_critical_tasks()

    def _get_edf_vd_x(self):
        u_lo_lo, u_lo_hi = 0, 0
        for high_critical_task in self.high_criticality_queue:
            u_lo_hi += high_critical_task.little_computation_time / high_critical_task.period
        for low_criticality_task in self.low_criticality_queue:
            u_lo_lo += low_criticality_task.computation_time / low_criticality_task.period
        edf_vd_x = u_lo_hi / (1 - u_lo_lo)
        return round(edf_vd_x, 2)

    def execute(self):
        while True:
            self._schedule_task()
            self.current_time += 1

    def _schedule_task(self, current_time):
        self._handle_done_tasks()
        tasks = self._get_tasks_by_deadline_ordering()

    def _get_tasks_by_deadline_ordering(self):
        if self.mode == configs.Mode.NORMAL:
            return sorted(self.high_criticality_queue + self.low_criticality_queue, key=lambda task: task.deadline)
        return sorted(self.high_criticality_queue, key=lambda task: task.period)

    def _filter_eligible_tasks(self):
        pass

    def assign_to_core(self):
        pass

    def _handle_done_tasks(self):
        pass

    def _update_high_critical_tasks(self):
        for high_criticality_task in self.high_criticality_queue:
            high_criticality_task.virtual_deadline = math.ceil(self.edf_vd_x * high_criticality_task.deadline)
