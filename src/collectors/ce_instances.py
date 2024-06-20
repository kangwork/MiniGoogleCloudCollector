from google.cloud import compute_v1
from utils.resource import Resource
from collectors.collector import Collector
from utils.decorators import method_error_handler_decorator
from models.ce_instance import CEInstance


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

    @method_error_handler_decorator
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
                    CEInstance.from_gcp_object(instance)
                    for instance in instances_scoped_list.instances
                )

        return all_instances

    @method_error_handler_decorator
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
        return CEInstance.from_gcp_object(instance_client.get(request=request))

    @method_error_handler_decorator
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
            instances.append(CEInstance.from_gcp_object(instance))
        return instances
