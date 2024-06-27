from random import randint

from models import Resource


def generate_resources(count_of_resources):
    resources = []
    for _ in range(count_of_resources):
        capacity = count_of_resources * 2
        resource = Resource(capacity)
        resources.append(resource)
    return resources
