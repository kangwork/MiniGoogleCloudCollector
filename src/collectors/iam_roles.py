from google.cloud import iam_admin_v1 as iam
from collectors.collector import Collector
from utils.decorators import error_handler_decorator
from models.iam_role import IAMRole


# ==========================================================================
# Collector class
class IAMRoleCollector(Collector):
    def __init__(self, credentials=None):
        super().__init__(__name__, credentials)

    @classmethod
    def get_route_messages(self) -> str:
        route_messages = {
            "/iam/roles": ("List all roles in your project.", "/iam/roles"),
            "/iam/roles/ROLE_ID": (
                "Get details of a specific role.",
                "/iam/roles/123456789",
            ),
        }
        return super().get_route_messages(route_messages)

    @error_handler_decorator
    def collect_resource(self, role_id: int) -> IAMRole:
        """
        Get a role's details

        :param role_id, int, the role ID

        :return: dict, the role's details"""
        role_name = f"projects/{self.project_id}/roles/{str(role_id)}"
        client = iam.IAMClient(credentials=self.credentials)
        request = iam.GetRoleRequest(name=role_name)
        response = client.get_role(request=request)
        return IAMRole.from_gcp_object(response)

    @error_handler_decorator
    def collect_resources(self) -> list[IAMRole]:
        """
        Get all roles in a project

        :param project_id: str, the project ID

        :return: list, all roles in the project
        """
        client = iam.IAMClient(credentials=self.credentials)
        request = iam.ListRolesRequest(parent=f"projects/{self.project_id}")
        response = client.list_roles(request=request)
        roles = [IAMRole.from_gcp_object(role) for role in response.roles]
        return roles

    def __str__(self):
        return "IAMRoleCollector"
