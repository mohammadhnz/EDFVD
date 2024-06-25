import math
from typing import List

import configs
from models import HighCriticalityTask, LowCriticalityTask, BaseTask


class Simulator:
    def __init__(self, high_criticality_tasks, low_criticality_tasks, resources):
        self.mode = configs.Mode.NORMAL
        self.high_criticality_tasks = high_criticality_tasks
        self.low_criticality_tasks = low_criticality_tasks
        self.resources = resources
        self.current_time = 0
        self.cpu_count = 0
        self.edf_vd_x = self._get_edf_vd_x()
        self._update_high_critical_tasks()
        self.currently_assigned_tasks = [None for i in range(self.cpu_count)]

    def _get_edf_vd_x(self):
        u_lo_lo, u_lo_hi = 0, 0
        for high_critical_task in self.high_criticality_tasks:
            u_lo_hi += high_critical_task.little_computation_time / high_critical_task.period
        for low_criticality_task in self.low_criticality_tasks:
            u_lo_lo += low_criticality_task.computation_time / low_criticality_task.period
        edf_vd_x = u_lo_hi / (1 - u_lo_lo)
        return round(edf_vd_x, 2)

    def execute(self):
        while self.current_time < 10 ** 9:
            self._update_mode()
            self._handle_done_tasks()
            tasks = self._get_scheduled_tasks()
            self.assign_to_core(tasks)
            self.current_time += 1

    def _get_scheduled_tasks(self):
        tasks = self._get_tasks_by_deadline_ordering()
        tasks = list(
            filter(
                self._is_task_eligible_by_msrp, tasks
            )
        )
        return tasks

    def _handle_done_tasks(self):
        for i in range(len(self.currently_assigned_tasks)):
            task = self.currently_assigned_tasks[i]
            if isinstance(task, BaseTask) and task.is_finished(self.mode):
                task.advanced_forward_job()
                self.currently_assigned_tasks[i] = None

    def _get_tasks_by_deadline_ordering(self):
        high_criticality_queue = list(
            filter(lambda task: task.is_active(), self.high_criticality_tasks)
        )
        low_criticality_queue = list(
            filter(lambda task: task.is_active(), self.low_criticality_tasks)
        )
        if self.mode == configs.Mode.NORMAL:
            return sorted(high_criticality_queue + low_criticality_queue, key=lambda task: task.get_deadline(self.mode))
        return sorted(high_criticality_queue, key=lambda task: task.get_deadline(self.mode))

    def _is_task_eligible_by_msrp(self, task):
        return True

    def assign_to_core(self, tasks):
        self._disable_low_critical_tasks_in_overrun()

        self._assign_scheduled_tasks(tasks)

        self._advance_forward_tasks()

    def _disable_low_critical_tasks_in_overrun(self):
        if self.mode == configs.Mode.OVERRUN:
            for i in range(self.cpu_count):
                if not self.currently_assigned_tasks[i]:
                    continue
                if isinstance(self.currently_assigned_tasks[i], LowCriticalityTask):
                    self.currently_assigned_tasks[i] = None

    def _assign_scheduled_tasks(self, tasks):
        not_assigned_tasks = []
        for task in tasks:
            if task not in self.currently_assigned_tasks:
                not_assigned_tasks.append(task)
        for task in not_assigned_tasks:
            for index in range(len(self.currently_assigned_tasks)):
                currently_assigned_task = self.currently_assigned_tasks[index]
                if (not currently_assigned_task) or (task.get_deadline() < currently_assigned_task.get_deadline()):
                    self.currently_assigned_tasks[index] = task
                    break

    def _advance_forward_tasks(self):
        for task in self.currently_assigned_tasks:
            if not task:
                continue
            task.calculate()

    def _update_high_critical_tasks(self):
        for high_criticality_task in self.high_criticality_tasks:
            high_criticality_task.virtual_deadline = math.ceil(self.edf_vd_x * high_criticality_task.deadline)

    def _update_mode(self):
        for task in self.high_criticality_tasks:
            if task.is_active() and task.virtual_deadline <= self.current_time:
                self.mode = configs.Mode.OVERRUN
                return
        self.mode = configs.Mode.NORMAL
