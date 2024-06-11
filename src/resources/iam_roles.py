from google.cloud import iam_admin_v1 as iam
from utils.credentials import get_credentials
from utils.logging import get_console_logger
from utils.resource import Resource
from utils.collector import Collector

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
    def __init__(self):
        super().__init__(__name__)

    def get_route_messages(self) -> str:
        route_messages = {
            "/iam/roles": ("List all roles in your project.", "/iam/roles"),
            "/iam/roles/ROLE_ID": ("Get details of a specific role.", "/iam/roles/123456789")
        }
        return super().get_route_messages(route_messages)

    def collect_resource(self, role_id: int) -> Role | int:
        """
        Get a role's details
        
        :param role_id, int, the role ID
        
        :return: dict, the role's details"""
        credentials = get_credentials()
        project_id = credentials.project_id
        role_name = f'projects/{project_id}/roles/{str(role_id)}'
        try:
            client = iam.IAMClient(credentials=credentials)
            request = iam.GetRoleRequest(name=role_name)
            response = client.get_role(request=request)
            return Role(response)
        except Exception as e:
            self.logger.add_error(f"collect_resource(role_id={role_id}): {str(e)}")
            return e.code

    def collect_resources(self) -> list[Role] | int:
        """
        Get all roles in a project
        
        :param project_id: str, the project ID

        :return: list, all roles in the project
        """
        credentials = get_credentials()
        project_id = credentials.project_id
        try:
            client = iam.IAMClient(credentials=credentials)
            request = iam.ListRolesRequest(parent=f'projects/{project_id}')
            response = client.list_roles(request=request)
            roles = [Role(role) for role in response.roles]
            return roles
        except Exception as e:
            self.logger.add_error(f"collect_resources(): {str(e)}")
            return e.code


# ==========================================================================
# Main function
if __name__ == "__main__":
    logger = get_console_logger()
    logger.add_warning("This app cannot be run directly. Please run the main.py file.")
    logger.add_info("Exiting.")
    exit()


