import json
import random

from algorithms import generate_task, generate_resources, add_resource_usage
from models import Simulator
import configs
from models.core import Core

import matplotlib.pyplot as plt

from models.exceptions import PanicModeException


def initialize():
    average_utilizations_per_file = []  # Stores average utilizations for each file
    mapping_feasibilities = []          # Stores mapping feasibility for each file

    for i in range(1, 7):
        with open(configs.FILE_TO_BE_EXECUTED.format(i=i), 'r') as file:
            data = json.load(file)
        count_of_cores = int(data["count_of_cores"])
        core_utilization = float(data["core_utilization"])
        count_of_tasks = int(data["count_of_tasks"])
        ratio = float(data["ratio"])
        total_average_utilizations = []  # Stores utilizations for each iteration
        succeed, failed = 0, 0
        count_of_resources = count_of_cores
        resources = generate_resources(count_of_resources)

        for j in range(10):
            # Assuming generate_task, generate_resources, add_resource_usage, Core, Simulator are defined properly
            hc_tasks, lc_tasks = generate_task(core_utilization, count_of_cores, count_of_tasks, ratio)
            hc_tasks, lc_tasks = add_resource_usage(hc_tasks, lc_tasks, resources)
            cores = [Core(core_utilization) for _ in range(count_of_cores)]
            simulator = Simulator(hc_tasks, lc_tasks, resources, cores)
            try:
                average_utilization, failed = simulator.execute()
                total_average_utilizations.append(average_utilization)
                if not failed:
                    succeed += 1
            except ZeroDivisionError:
                failed += 1
            except IndexError:
                failed += 1
            except PanicModeException:
                failed += 1

        # Store data for plotting
        average_utilization_per_file = sum(total_average_utilizations) / len(total_average_utilizations) if len(total_average_utilizations) > 0 else 0
        average_utilizations_per_file.append(average_utilization_per_file)
        mapping_feasibility = succeed / 10
        mapping_feasibilities.append(mapping_feasibility)
        print(f"File {i}: Mapping Feasibility = {mapping_feasibility}")

    # Plotting the average utilizations
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, 7), average_utilizations_per_file, marker='o')
    plt.title("Average Utilizations per scenario")
    plt.xlabel("File Number")
    plt.ylabel("Average Utilization")
    plt.grid(True)
    plt.xticks(range(1, 7))  # Assuming files are from 1 to 6
    plt.show()

    # Plotting Mapping Feasibility
    plt.figure(figsize=(10, 5))
    plt.bar(range(1, 7), mapping_feasibilities, color='lightblue')
    plt.title("Mapping Feasibility")
    plt.xlabel("Scenario Number")
    plt.ylabel("Feasibility Ratio")
    plt.xticks(range(1, 7))  # Assuming files are from 1 to 6
    plt.show()

initialize()