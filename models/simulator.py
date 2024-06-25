import math
from typing import List

import configs
from models import HighCriticalityTask, LowCriticalityTask, Resource


class Simulator:
    def __init__(self, high_criticality_tasks, low_criticality_tasks, resources):
        self.mode = configs.Mode.NORMAL
        self.high_criticality_tasks = high_criticality_tasks
        self.low_criticality_tasks = low_criticality_tasks
        self.resources = resources
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
            task = self._schedule_tasks()
            self.assign_to_core(task)
            self.current_time += 1

    def _schedule_tasks(self):
        self._handle_done_tasks()
        tasks = self._get_tasks_by_deadline_ordering()
        tasks = list(
            filter(
                self._is_task_eligible_by_msrp, tasks
            )
        )
        return tasks[0]

    def _handle_done_tasks(self):
        for task in self.high_criticality_queue + self.low_criticality_queue:
            if task.is_finished(self.mode):
                task.advanced_forward_job()

    def _get_tasks_by_deadline_ordering(self):
        high_criticality_queue = list(
            filter(lambda task: task.is_active(), self.high_criticality_queue)
        )
        low_criticality_queue = list(
            filter(lambda task: task.is_active(), self.low_criticality_queue)
        )
        if self.mode == configs.Mode.NORMAL:
            return sorted(high_criticality_queue + low_criticality_queue, key=lambda task: task.get_deadline(self.mode))
        return sorted(high_criticality_queue, key=lambda task: task.get_deadline(self.mode))

    def _is_task_eligible_by_msrp(self, task):
        return True

    def assign_to_core(self, task):
        pass

    def _update_high_critical_tasks(self):
        for high_criticality_task in self.high_criticality_queue:
            high_criticality_task.virtual_deadline = math.ceil(self.edf_vd_x * high_criticality_task.deadline)
