from google.cloud import compute_v1
from utils.credentials import get_credentials
from utils.logging import get_console_logger, get_sub_file_logger
from utils.resource import Resource

logger = get_sub_file_logger(__name__)

# 0. A class to represent a VM Instance
class VMInstance(Resource):
    """
    A class to represent a VM Instance

    Attributes:
    - name: str, the instance name
    - zone: str, the instance zone
    - machine_type: str, the instance machine type
    - status: str, the instance status
    - creation_time: datetime, the instance creation time
    - disks: list, the instance disks
    - network_interfaces: list, the instance network interfaces
    - metadata: dict, the instance metadata
    """
    def __init__(self, resource: dict = None):
        super().__init__()
        self.name = None
        self.zone = None
        self.machine_type = None
        self.status = None
        self.creation_time = None
        self.disks = None
        self.network_interfaces = None
        self.metadata = None
        if resource:
            self.set_resource(resource)
    

    def set_resource(self, resource: dict):
        super().set_resource(resource)
        self.name = resource.name
        self.zone = resource.zone
        self.machine_type = resource.machine_type
        self.status = resource.status
        self.creation_time = resource.creation_timestamp
        self.disks = resource.disks
        self.network_interfaces = resource.network_interfaces
        self.metadata = resource.metadata


    def __str__(self):
        """
        Simplify the object representation for listing (instance name)
        """
        return f"Zone: {self.zone}, Name: {self.name}"


    # 1. A function to return route messages
    def get_route_messages(self) -> str:
        return """

            Visit /vm/instances to list all VM instances in your project. Include zone as a query parameter.
        
            Visit /vm/instances/ZONE to list all VM instances in a specific zone in your project. Include zone as a query parameter.
            (Example: /vm/instances/us-west1-b)
            
            Visit /vm/instances/ZONE/INSTANCE_NAME to get details of a specific VM instance.
            (Example: /vm/instances/us-west1-b/mini-collector-instance)
            
            """

# =============================================================================
# 2. Helper functions to get instance objects (VM Instances)
# 2-1. A function to list all instances in a project
def collect_resources() -> list[VMInstance] | int:
    """
    List all instances in a project

    :param project_id: str, the project ID

    :return: list of instances[VMInstance]
    """
    credentials = get_credentials()
    project_id = credentials.project_id

    try:
        instance_client = compute_v1.InstancesClient(credentials=credentials)
        instances = []
        for (zone_info, instances_scoped_list) in instance_client.aggregated_list(project=project_id):
            zone_instances, warning = instances_scoped_list.instances, instances_scoped_list.warning
            if warning:
                continue
            else:
                for instance in zone_instances:
                    instances.append(VMInstance(instance))
            # it's in form of 'zones/ZONENAME', so extract the ZONENAME
            # zone_name = zone_info.split('/')[-1]
            # instances_in_zone = collect_resources_in_zone(zone_name)
            # instances.extend(instances_in_zone)
        return instances
    except Exception as e:
        logger.add_error(f"collect_resources(): {str(e)}")
        return e.code


# 2-2. A function to get details of a specific instance
def collect_resource(zone: str, instance_name: str) -> VMInstance | int:
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
        return VMInstance(instance_client.get(request=request))
    except Exception as e:
        logger.add_error(f"collect_resource(zone={zone}, instance_name:{instance_name}): {str(e)}")
        return e.code
    

# 2-3. A function to list all instances in a project in a specific zone
def collect_resources_in_zone(zone: str) -> list[VMInstance] | int:
    """
    List all instances in a project

    :param project_id: str, the project ID
    :param zone: str, the zone

    :return: list of instances[VMInstance]
    """
    credentials = get_credentials()
    project_id = credentials.project_id

    try:
        instance_client = compute_v1.InstancesClient(credentials=credentials)
        request = compute_v1.ListInstancesRequest(project=project_id, zone=zone)  # NOTE: Check if zone is required  --> Yes, it is required if we use this method
        instances = []
        for instance in instance_client.list(request=request):
            instances.append(VMInstance(instance))
        return instances
    except Exception as e:
        logger.add_error(f"collect_resources_in_zone(zone={zone}): {str(e)}")
        return e.code


# =============================================================================
# 3. Main function
if __name__ == '__main__':
    logger = get_console_logger()
    logger.add_warning("This app cannot be run directly. Please run the main.py file.")
    logger.add_info("Exiting.")
    exit(0)