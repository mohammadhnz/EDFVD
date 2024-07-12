from collections import defaultdict
from typing import Union

from models import BaseTask


class Core:
    def __init__(self, utilization):
        self.task_set = list()
        self.resource_congestion = defaultdict(float)
        self.current_task: Union[BaseTask, None] = None
        self.utilization = utilization
        self.is_busy_waiting = False
    @property
    def wfd(self):
        return sum([task.get_utilization() for task in self.task_set])

    def add_task(self, task: BaseTask):
        for resource, count in task.resource_demands.items():
            self.resource_congestion[resource] += count

        self.task_set.append(task)

    def busy_wait(self):
        self.is_busy_waiting = True

    def run(self):
        self.is_busy_waiting = False
