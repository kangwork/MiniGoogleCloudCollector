from google.cloud import iam_admin_v1 as iam
from utils.credentials import get_credentials
from utils.logging import Logger, setup_logger

### This module is divided into 5 categories of functions:
# 1. A function to return route messages (used in the ../main.py)
#    - get_route_messages(default_project_id: str) -> str
# 2. Helper functions to get role objects
#     - _get_role(project_id: str, role_id: int) -> dict
#     - _get_all_roles(project_id: str) -> list
#
# 3. Helper functions to stringify given role objects
#     - _stringify_role(role: dict, index: int = None, total: int = None) -> str
#     - _stringify_roles(roles: list) -> str
#
# 4. Wrapper functions to get and print role(s) in a project, using the helper functions
#     - print_role(project_id: str, role_id: int) -> str | None
#     - print_all_roles(project_id: str) -> str | None
#
# 5. Main function
###

### 1. A function to return route messages

def get_route_messages(default_project_id: str) -> str:
    return f"""

        Visit /iam/roles to list all IAM roles in your project. 
        (Example: /iam/roles?project_id={default_project_id})

        Visit /iam/roles/ROLE_ID to get details of a specific IAM role.
        (Example: /iam/roles/609?project_id={default_project_id})
        
        """

# =============================================================================
### 2. Helper functions to get role objects
# A function to get a role's details
def _get_role(role_id: int, logger: Logger) -> dict:
    """
    Get a role's details
    
    :param role_id, int, the role ID
    
    :return: dict, the role's details"""
    credentials = get_credentials()
    project_id = credentials.project_id
    role_name = f'projects/{project_id}/roles/{str(role_id)}'
    logger.add_info(f"Getting role: {role_name}")
    try:
        client = iam.IAMClient(credentials=credentials)
        request = iam.GetRoleRequest(name=role_name)
        response = client.get_role(request=request)
        return response
    except Exception as e:
        logger.add_error(f"Failed to get role: {str(e)}")
        return None


# A function to get all roles in a project
def _get_all_roles(logger: Logger) -> list:
    """
    Get all roles in a project
    
    :param project_id: str, the project ID

    :return: list, all roles in the project
    """
    credentials = get_credentials()
    project_id = credentials.project_id
    logger.add_info("Getting all roles in the project.")
    try:
        client = iam.IAMClient(credentials=credentials)
        request = iam.ListRolesRequest(parent=f'projects/{project_id}')
        response = client.list_roles(request=request)
        return response.roles
    except Exception as e:
        logger.add_error(f"Failed to get all roles: {str(e)}")
        return None


# ==========================================================================
### 3. Helper functions to stringify given role objects
# A function to print a role's details
def _stringify_role(role: dict, index: int = None, total: int = None) -> str:
    """
    Print a role's details
    
    :param role: role dict(object of iam.Role), the role object
    """
    if index is not None and total is not None:
        message = f"\n[Role {index+1} of {total}]"
    else:
        message = "\n=====================================\n"
        message += "[Role]"
    message += (f"""
    Role: {role.name}
    Title: {role.title}
    Description:
    {role.description}
=====================================""")
    return message


# A function to print a list of roles
def _stringify_roles(roles: list) -> str:
    """
    Print all roles in a project

    :param project_id: str, the project ID
    """
    message = "\n====================================="
    for i in range(len(roles)):
        message += _stringify_role(roles[i], i, len(roles))
    return message


# ==========================================================================
### 4. Wrapper functions to get and print role(s) in a project, using the helper functions
def print_role(role_id: int, logger: Logger) -> str | None:
    """
    Print a role's details
    
    :param role_id, int, the role ID
    """
    role = _get_role(role_id, logger)
    message = _stringify_role(role)
    # logger.add_info(message)
    return message

def print_all_roles(logger: Logger) -> str | None:
    """
    Print all roles in a project

    :param project_id: str, the project ID
    """
    roles = _get_all_roles(logger)
    logger.add_info("Printing all roles in the project.")
    message = _stringify_roles(roles)
    # logger.add_info(message)
    return message


# ==========================================================================
# 5. Main function
if __name__ == "__main__":
    # 1.Setup the logger
    logger = setup_logger()

    # 2. Define the project ID
    project_id = "bluese-cloudone-20200113"

    # Part 1: List all resources in a project
    print_all_roles(project_id, logger)  # Checking if the print_all_roles function works

    
    # Part 2: Retrieve a specific resource's data
    role_title1 = "mini-collector-resource-viewer"
    role_id1 = 609

    role_title2 = "mini-collector-iam-viewer"
    role_id2 = 261

    print_role(project_id=project_id, role_id=role_id1, logger=logger)  # Checking if the print_role function works

    
    logger.add_info("Exiting.")
    exit()


