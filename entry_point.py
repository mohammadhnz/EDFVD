import json

import algorithms
import configs


def initialize():
    with open(configs.FILE_TO_BE_EXECUTED, 'r') as file:
        data = json.load(file)
        count_of_cores = int(data["count_of_cores"])
        core_utilization = float(data["core_utilization"])
        count_of_tasks = int(data["count_of_tasks"])
        ratio = float(data["ratio"])

        hc_tasks, lc_tasks = algorithms.generate_task(core_utilization, count_of_cores, count_of_tasks, ratio)

        assert min([item.little_computation_time for item in hc_tasks]) > 0
        assert min([item.big_computation_time for item in hc_tasks]) > 0
        assert min([item.computation_time for item in lc_tasks]) > 0

        count_of_resources = int(data["count_of_resources"])
        resources = algorithms.generate_resources(count_of_resources)
