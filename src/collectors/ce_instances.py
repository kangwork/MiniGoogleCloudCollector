from google.cloud import compute_v1
from utils.resource import Resource
from collectors.collector import Collector
from utils.decorators import error_handler_decorator


# ==========================================================================
# Resource class
class CEInstance(Resource):
    """
    A class to represent a CE(Compute Engine) Instance

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

    def __init__(self, resource: dict):
        super().__init__(resource)
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


# =============================================================================
# Collector class
class CEInstanceCollector(Collector):
    def __init__(self, credentials=None):
        super().__init__(__name__, credentials)

    @classmethod
    def get_route_messages(self) -> str:
        route_messages = {
            "/ce/instances": (
                "List all Compute Engine instances in your project.",
                "/ce/instances",
            ),
            "/ce/instances/ZONE": (
                "List all Compute Engine instances in a specific zone in your project. Include zone as a query parameter.",
                "/ce/instances/us-west1-b",
            ),
            "/ce/instances/ZONE/INSTANCE_NAME": (
                "Get details of a specific Compute Engine instance.",
                "/ce/instances/us-west1-b/mini-collector-instance",
            ),
        }
        return super().get_route_messages(route_messages)

    @error_handler_decorator
    def collect_resources(self) -> list[CEInstance]:
        """
        List all instances in a project

        :param project_id: str, the project ID

        :return: list of instances[CEInstance]
        """
        instance_client = compute_v1.InstancesClient(credentials=self.credentials)
        all_instances = []

        for _, instances_scoped_list in instance_client.aggregated_list(
            project=self.project_id
        ):

            if instances_scoped_list.warning:
                continue
            else:
                all_instances.extend(
                    CEInstance(instance) for instance in instances_scoped_list.instances
                )

        return all_instances

    @error_handler_decorator
    def collect_resource(self, zone: str, instance_name: str) -> CEInstance:
        """
        Get details of a specific instance

        :param project_id: str, the project ID
        :param zone: str, the zone
        :param instance_name: str, the instance name

        :return: instance details
        """
        instance_client = compute_v1.InstancesClient(credentials=self.credentials)
        request = compute_v1.GetInstanceRequest(
            project=self.project_id, zone=zone, instance=instance_name
        )
        return CEInstance(instance_client.get(request=request))

    @error_handler_decorator
    def collect_resources_in_zone(self, zone: str) -> list[CEInstance]:
        """
        List all instances in a project

        :param project_id: str, the project ID
        :param zone: str, the zone

        :return: list of instances[CEInstance]
        """
        instance_client = compute_v1.InstancesClient(credentials=self.credentials)
        request = compute_v1.ListInstancesRequest(project=self.project_id, zone=zone)
        instances = []
        for instance in instance_client.list(request=request):
            instances.append(CEInstance(instance))
        return instances
