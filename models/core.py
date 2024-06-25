from collections import defaultdict
from typing import Union

from models import BaseTask


class Core:
    def __init__(self):
        self.wfd = 0
        self.task_history = list()
        self.resource_congestion = defaultdict(float)
        self.current_task: Union[BaseTask, None] = None

    def add_task(self, task: BaseTask):
        self.current_task = task
        self.task_history.append(task)

    def advance_forward(self, mode):
        if not self.current_task:
            return
        for resource, count in self.current_task.resource_demands.items():
            self.resource_congestion[resource] += count / self.current_task.get_computation_time(mode)
