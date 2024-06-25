import random
from typing import List

from models import HighCriticalityTask, LowCriticalityTask


def add_resource_usage(hc_tasks: List[HighCriticalityTask], lc_tasks: List[LowCriticalityTask], resources):
    for task in hc_tasks:
        computation_time = task.little_computation_time
        for resource in resources:
            resource_demand = min(computation_time, random.randint(0, resource.capacity))
            task.resource_demands[resource] = resource_demand
            computation_time -= resource_demand

    for task in lc_tasks:
        computation_time = task.computation_time
        for resource in resources:
            resource_demand = min(computation_time, random.randint(0, resource.capacity))
            task.resource_demands[resource] = resource_demand
            computation_time -= resource_demand

    return hc_tasks, lc_tasks
