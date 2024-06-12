from google.cloud import iam_admin_v1 as iam
from utils.logging import get_console_logger
from utils.resource import Resource
from utils.collector import Collector
from utils.decorators import error_handler_decorator

# ==========================================================================
# Resource class
class Role(Resource):
    """
    A class to represent a Role

    Attributes:
    - name: str, the role name
    - title: str, the role title
    - description: str, the role description
    - stage: str, the role stage
    - included_permissions: list, the role's included permissions
    """
    def __init__(self, resource: dict):
        super().__init__(resource)
        self.name = resource.name
        self.title = resource.title
        self.description = resource.description
        self.stage = resource.stage
        self.included_permissions = resource.included_permissions
    

    def __str__(self):
        """
        Simplify the object representation for listing (role id)
        """
        return self.name


# ==========================================================================
# Collector class
class IAMRoleCollector(Collector):
    def __init__(self, credentials=None):
        super().__init__(__name__, credentials)

    def get_route_messages(self) -> str:
        route_messages = {
            "/iam/roles": ("List all roles in your project.", "/iam/roles"),
            "/iam/roles/ROLE_ID": ("Get details of a specific role.", "/iam/roles/123456789")
        }
        return super().get_route_messages(route_messages)

    @error_handler_decorator
    def collect_resource(self, role_id: int) -> Role:
        """
        Get a role's details
        
        :param role_id, int, the role ID
        
        :return: dict, the role's details"""
        role_name = f'projects/{self.project_id}/roles/{str(role_id)}'
        client = iam.IAMClient(credentials=self.credentials)
        request = iam.GetRoleRequest(name=role_name)
        response = client.get_role(request=request)
        return Role(response)

    @error_handler_decorator
    def collect_resources(self) -> list[Role]:
        """
        Get all roles in a project
        
        :param project_id: str, the project ID

        :return: list, all roles in the project
        """
        client = iam.IAMClient(credentials=self.credentials)
        request = iam.ListRolesRequest(parent=f'projects/{self.project_id}')
        response = client.list_roles(request=request)
        roles = [Role(role) for role in response.roles]
        return roles


