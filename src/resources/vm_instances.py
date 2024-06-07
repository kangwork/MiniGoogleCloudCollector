from google.cloud import compute_v1
from utils.credentials import get_credentials
from fastapi.exceptions import HTTPException
from utils.logging import Logger, setup_logger

# 1. A function to return route messages
def get_route_messages(default_project_id: str) -> str:
    return f"""
    
        Visit /vm/instances to list all VM instances in your project. Include zone as a query parameter.
        (Example: /vm/instances?zone=us-west1-b)
        
        Visit /vm/instances/ZONE/INSTANCE_NAME to get details of a specific VM instance.
        (Example: /vm/instances/us-west1-b/mini-collector-instance)
        
        """

# =============================================================================
# 2. Helper functions to get instance objects (VM Instances)

# 2-1. A function to list all instances in a project
def list_instances(zone: str) -> dict:
    """
    List all instances in a project

    :param project_id: str, the project ID
    :param zone: str, the zone

    :return: list of instances
    """
    credentials = get_credentials()
    project_id = credentials.project_id

    try:
        instance_client = compute_v1.InstancesClient(credentials=credentials)
        request = compute_v1.ListInstancesRequest(project=project_id, zone=zone)  # NOTE: Check if zone is required  --> Yes, it is required
        return {"instances": instance_client.list(request=request)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Failed to retrieve buckets: {str(e)}")


# 2-2. A function to get details of a specific instance
def get_instance_details(zone: str, instance_name: str) -> dict:
    """
    Get details of a specific instance

    :param project_id: str, the project ID
    :param zone: str, the zone
    :param instance_name: str, the instance name

    :return: instance details
    """
    credentials = get_credentials()
    project_id = credentials.project_id

    try:
        instance_client = compute_v1.InstancesClient(credentials=credentials)
        request = compute_v1.GetInstanceRequest(project=project_id, zone=zone, instance=instance_name)
        return instance_client.get(request=request)
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Failed to retrieve buckets: {str(e)}")


# =============================================================================
# 3. Main function
if __name__ == '__main__':
    logger = Logger()
    setup_logger(logger, to_file=False)
    logger.add_info("This app cannot be run directly. Please run the main.py file.")
    logger.add_info("Exiting.")
    exit()

    # For DEBUGGING purposes =================================================
    # zone = "us-west1-b"
    # instance_name = "mini-collector-instance"

    # # Part 1: Retrieve a specific resource's data
    # instance = get_instance_details(zone, instance_name)
    # print(instance)  # Checking if the get_instance_details function works

    # # Part 2: List all resources in a project
    # instances = list_instances(zone)
    # for instance in instances:
    #     print(instance.name)  # Checking if the list_instances function works
    #     details = get_instance_details(zone, instance.name)
    #     print(details)

    # # Exit for now
    # print('Exiting.')
    # exit(0)