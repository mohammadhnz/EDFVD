from models import Resource


def generate_resources(count_of_resources):
    resources = []
    for _ in range(count_of_resources):
        resource = Resource()
        resources.append(resource)
    return resources
