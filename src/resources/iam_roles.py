from google.cloud import iam_admin_v1 as iam
from utils.credentials import get_credentials
from utils.logging import get_console_logger, get_sub_file_logger
from utils.resource import Resource


### This module is divided into 5 categories of functions:
# 0. A class to represent a Role
#
# 1. A function to return route messages (used in the ../main.py)
#    - get_route_messages(default_project_id: str) -> str
# 2. Helper functions to get role objects
#     - _get_role(project_id: str, role_id: int) -> dict
#     - _get_all_roles(project_id: str) -> list
#
# -. Helper functions to stringify given role objects (deprecated)
#     - _stringify_role(role: dict, index: int = None, total: int = None) -> str
#     - _stringify_roles(roles: list) -> str
#
# 4. Wrapper functions to get and print role(s) in a project, using the helper functions
#     - print_role(project_id: str, role_id: int) -> str | None
#     - print_all_roles(project_id: str) -> str | None
#
# 5. Main function
###

logger = get_sub_file_logger(__name__)

# ==========================================================================
# 0. A class to represent a Role
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
    def __init__(self, role: dict):
        super().__init__(role)
        self.name = role.name
        self.title = role.title
        self.description = role.description
        self.stage = role.stage
        self.included_permissions = role.included_permissions

    def __str__(self):
        """
        Simplify the object representation for listing (role id)
        """
        return self.name

# ==========================================================================
### 1. A function to return route messages
def get_route_messages(default_project_id: str) -> str:
    return f"""

        Visit /iam/roles to list all IAM roles in your project. 
        (Example: /iam/roles)

        Visit /iam/roles/ROLE_ID to get details of a specific IAM role.
        (Example: /iam/roles/609)
        
        """

# =============================================================================
### 2. Helper functions to get role objects

# 2-1. A function to get a role's details
def collect_resource(role_id: int) -> Role | int:
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
        logger.add_error(f"collect_resource(role_id={role_id}): {str(e)}")
        return e.code


# 2-2. A function to get all roles in a project
def collect_resources() -> list[Role] | int:
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
        logger.add_error(f"collect_resources(): {str(e)}")
        return e.code


# ==========================================================================
### 3. Helper functions to stringify given role objects (deprecated)

# ==========================================================================
### 4. Wrapper functions to get and print role(s) in a project, using the helper functions (deprecated)

# ==========================================================================
# 5. Main function
if __name__ == "__main__":
    logger = get_console_logger()
    logger.add_warning("This app cannot be run directly. Please run the main.py file.")
    logger.add_info("Exiting.")
    exit()


