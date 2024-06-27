import math
from fractions import Fraction
from typing import List

import configs
from models import HighCriticalityTask, LowCriticalityTask, BaseTask


class Simulator:
    def __init__(self, high_criticality_tasks, low_criticality_tasks, resources, cores):
        self.mode = configs.Mode.NORMAL
        self.high_criticality_tasks = high_criticality_tasks
        self.low_criticality_tasks = low_criticality_tasks
        self.resources = resources
        self.current_time = 0
        self.cpu_count = len(cores)
        self.edf_vd_x = self._get_edf_vd_x()
        self._update_high_critical_tasks()
        self.currently_assigned_tasks = {core: None for core in cores}
        self.srp_table = self._generate_srp_table()
        self.system_preemption_level = math.inf

    def _get_edf_vd_x(self):
        u_lo_lo, u_lo_hi = 0, 0
        for high_critical_task in self.high_criticality_tasks:
            u_lo_hi += high_critical_task.little_computation_time / high_critical_task.period
        for low_criticality_task in self.low_criticality_tasks:
            u_lo_lo += low_criticality_task.computation_time / low_criticality_task.period
        edf_vd_x = u_lo_hi / (1 - u_lo_lo)
        return round(edf_vd_x, 4)

    def execute(self):
        self._assign_to_core()
        total_usage_of_cores = 0
        failed = False
        try:
            while self.current_time < 10 ** 5:
                self._update_system_preemption_level()
                self._update_mode()
                self._handle_done_tasks()
                self._disable_low_critical_tasks_in_overrun()
                self._scheduled_tasks()
                self._advance_forward_tasks()
                self.current_time += 1
                total_usage_of_cores += sum([(1 if task is not None else 0) for _, task in self.currently_assigned_tasks.items()])
        except Exception:
            failed = True
        return total_usage_of_cores / (self.current_time * self.cpu_count), failed

    def _scheduled_tasks(self):
        for core, currently_assigned_task in self.currently_assigned_tasks.items():
            tasks = self._get_tasks_by_deadline_ordering(core)
            tasks = list(
                filter(
                    lambda task: task.get_preemption_level(self.srp_table) < self.system_preemption_level, tasks
                )
            )
            if tasks:
                self.currently_assigned_tasks[core] = tasks[0]

    def _handle_done_tasks(self):
        for core, task in self.currently_assigned_tasks.items():
            if isinstance(task, BaseTask) and task.is_finished(self.mode):
                # print("Done task", "current_job", str(task.current_job), task)
                task.advanced_forward_job()
                self.currently_assigned_tasks[core] = None
            elif isinstance(task, BaseTask) and task.is_deadline_missed(self.mode, self.current_time):
                if isinstance(task, HighCriticalityTask):
                    # print(self.current_time)
                    # print(self.mode)
                    # print(task.virtual_deadline)
                    raise Exception('Panic Mode')
                self.currently_assigned_tasks[core] = None
                task.advanced_forward_job()
                # print("Missed deadline", task)

    def _get_tasks_by_deadline_ordering(self, core):
        high_criticality_queue = list(
            filter(
                lambda task: task.is_active(self.current_time),
                [t for t in core.task_set if isinstance(t, HighCriticalityTask)]
            )
        )
        low_criticality_queue = list(
            filter(
                lambda task: task.is_active(self.current_time),
                [t for t in core.task_set if isinstance(t, LowCriticalityTask)]
            )
        )
        if self.mode == configs.Mode.NORMAL:
            return sorted(high_criticality_queue + low_criticality_queue, key=lambda task: task.get_deadline(self.mode))
        return sorted(high_criticality_queue, key=lambda task: task.get_deadline(self.mode))

    def _assign_to_core(self):
        for task in self.high_criticality_tasks + self.low_criticality_tasks:
            usable_cores = list(self.currently_assigned_tasks.keys())
            usable_cores = sorted(usable_cores, key=lambda core: self._calculate_congestion(core, task), reverse=True)
            usable_cores = [core for core in usable_cores if Fraction(task.get_utilization()) <= Fraction(core.utilization - core.wfd)]
            core = usable_cores[0]
            core.add_task(task)

    def _disable_low_critical_tasks_in_overrun(self):
        if self.mode != configs.Mode.OVERRUN:
            return
        for core, task in self.currently_assigned_tasks.items():
            if not task:
                continue
            if isinstance(task, LowCriticalityTask):
                self.currently_assigned_tasks[core] = None

    def _advance_forward_tasks(self):
        for core, task in self.currently_assigned_tasks.items():
            if not task:
                continue
            task.calculate()

    def _update_high_critical_tasks(self):
        for high_criticality_task in self.high_criticality_tasks:
            high_criticality_task.virtual_deadline = math.ceil(self.edf_vd_x * high_criticality_task.period)

    def _update_mode(self):
        for task in self.high_criticality_tasks:
            if task.is_active(self.current_time) and task.virtual_deadline <= self.current_time:
                self.mode = configs.Mode.OVERRUN
                return
        self.mode = configs.Mode.NORMAL

    def _generate_srp_table(self):
        srp_table = dict()
        total_tasks = self.high_criticality_tasks + self.low_criticality_tasks
        max_period = max([item.period for item in total_tasks])
        for resource in self.resources:
            srp_table[resource] = [
                min([task.period for task in total_tasks if task.resource_demands[resource] > i] + [max_period]) for i in range(resource.capacity + 1)
            ]
        return srp_table

    def _update_system_preemption_level(self):
        min(
            [task.get_preemption_level(self.srp_table) for _, task in self.currently_assigned_tasks.items() if task] + [math.inf]
        )

    def _calculate_congestion(self, core, task):
        resources = [resource for resource, count in task.resource_demands.items() if count > 0]
        return sum([core.resource_congestion[resource] for resource in resources])