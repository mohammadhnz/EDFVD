import json
import random

from algorithms import generate_task, generate_resources, add_resource_usage
from models import Simulator
import configs
from models.core import Core


def initialize():
    for i in range(1,7):
        with open(configs.FILE_TO_BE_EXECUTED.format(i=i), 'r') as file:
            data = json.load(file)
            count_of_cores = int(data["count_of_cores"])
            core_utilization = float(data["core_utilization"])
            count_of_tasks = int(data["count_of_tasks"])
            ratio = float(data["ratio"])
            succeed, failed = 0, 0
            average_utilizations = list()
            for i in range(10):
                hc_tasks, lc_tasks = generate_task(core_utilization, count_of_cores, count_of_tasks, ratio)

                assert min([item.little_computation_time for item in hc_tasks]) > 0
                assert min([item.big_computation_time for item in hc_tasks]) > 0
                assert min([item.computation_time for item in lc_tasks]) > 0

                count_of_resources = random.randint(2,6)
                resources = generate_resources(count_of_resources)

                hc_tasks, lc_tasks = add_resource_usage(hc_tasks, lc_tasks, resources)
                cores = [Core(core_utilization) for i in range(count_of_cores)]
                simulator = Simulator(hc_tasks, lc_tasks, resources, cores)
                try:
                    average_utilization = simulator.execute()
                    average_utilizations.append(average_utilization)
                    succeed += 1
                except Exception:
                    failed += 1
            print("Mapping Feasibility", succeed / 10)
            print(average_utilization)


initialize()