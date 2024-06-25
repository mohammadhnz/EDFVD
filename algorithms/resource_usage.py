import random
from typing import List

from models import HighCriticalityTask, LowCriticalityTask


def add_resource_usage(hc_tasks: List[HighCriticalityTask], lc_tasks: List[LowCriticalityTask], resources):
    for task in hc_tasks:
        computation_time = task.little_computation_time
        for _ in resources:
            resource_demand = random.randint(0, computation_time)
            task.resource_demands.append(resource_demand)
            computation_time -= resource_demand

    for task in lc_tasks:
        computation_time = task.computation_time
        for _ in resources:
            resource_demand = random.randint(0, computation_time)
            task.resource_demands.append(resource_demand)
            computation_time -= resource_demand

    return hc_tasks, lc_tasks
