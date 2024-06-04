from google.cloud import compute_v1
from credentials import get_credentials

# A function to list all instances in a project
def list_instances(project_id: str, zone: str):
    """
    List all instances in a project

    :param project_id: str, the project ID
    :param zone: str, the zone

    :return: list of instances
    """
    credentials = get_credentials()
    instance_client = compute_v1.InstancesClient(credentials=credentials)
    request = compute_v1.ListInstancesRequest(project=project_id, zone=zone)
    return instance_client.list(request=request)

# A function to get details of a specific instance
def get_instance_details(project_id: str, zone, instance_name):
    """
    Get details of a specific instance

    :param project_id: str, the project ID
    :param zone: str, the zone
    :param instance_name: str, the instance name

    :return: instance details
    """
    credentials = get_credentials()
    instance_client = compute_v1.InstancesClient(credentials=credentials)
    request = compute_v1.GetInstanceRequest(project=project_id, zone=zone, instance=instance_name)
    return instance_client.get(request=request)


if __name__ == '__main__':
    project_id = "bluese-cloudone-20200113"
    zone = "us-west1-b"
    instance_name = "mini-collector-instance"

    # Part 1: Retrieve a specific resource's data
    instance = get_instance_details(project_id, zone, instance_name)
    print(instance)  # Checking if the get_instance_details function works

    # Exit for now
    print('Exiting...')
    exit()

    # Part 2: List all resources in a project
    instances = list_instances(project_id, zone)
    for instance in instances:
        print(instance.name)  # Checking if the list_instances function works
        details = get_instance_details(project_id, zone, instance.name)
        print(details)