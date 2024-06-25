from random import randint

from models import Resource


def generate_resources(count_of_resources):
    resources = []
    for _ in range(count_of_resources):
        capacity = randint(1,10)
        resource = Resource(capacity)
        resources.append(resource)
    return resources
