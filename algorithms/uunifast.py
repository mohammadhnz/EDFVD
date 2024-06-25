from typing import List
from models import HighCriticalityTask, LowCriticalityTask
import random


def generate_task(core_utilization, number_of_cores, number_of_tasks, ratio) -> (List[HighCriticalityTask], List[LowCriticalityTask]):
    utilizations = []
    for i in range(number_of_cores):
        new_utilizations = _uunifast_algorithm(core_utilization, number_of_tasks // number_of_cores)
        utilizations.extend(new_utilizations)

    number_of_hc_tasks = int(number_of_tasks * ratio)
    hc_utilization = utilizations[:number_of_hc_tasks]
    lc_utilization = utilizations[number_of_hc_tasks:]

    hc_tasks = []
    for u in hc_utilization:
        period = random.randint(10000, 20000)
        little_computation_time = int(u * period)
        big_computation_time = random.randint(little_computation_time, period)
        hc_task = HighCriticalityTask(little_computation_time, big_computation_time, period)
        hc_tasks.append(hc_task)

    lc_tasks = []
    for u in lc_utilization:
        period = random.randint(100000, 200000)
        computation_time = int(u * period)
        lc_task = LowCriticalityTask(computation_time, period)
        lc_tasks.append(lc_task)

    return hc_tasks, lc_tasks


def _uunifast_algorithm(core_utilization, number_of_tasks) -> List:
    utilizations = []
    sum_u = core_utilization
    for i in range(number_of_tasks - 1):
        next_sum_u = sum_u * random.random() ** (core_utilization / (number_of_tasks - i))
        utilizations.append(sum_u - next_sum_u)
        sum_u = next_sum_u
    utilizations.append(sum_u)

    sets = []
    if all(ut <= core_utilization for ut in utilizations):
        sets.extend(utilizations)

    return sets
