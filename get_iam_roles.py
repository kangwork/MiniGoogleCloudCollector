from google.cloud import iam_admin_v1 as iam
from credentials import get_credentials

### This module is divided into 4 categories of functions:
# 1. Helper functions to get role objects
#     - _get_role(project_id: str, role_id: int) -> dict
#     - _get_all_roles(project_id: str) -> list
#
# 2. Helper functions to print given role objects
#     - _print_role(role: dict) -> None
#     - _print_roles(roles: list) -> None
#
# 3. Wrapper functions to get and print role(s) in a project, using the helper functions
#     - print_role(project_id: str, role_id: int) -> None
#     - print_all_roles(project_id: str) -> None
#
# 4. Main function
###


# =============================================================================
### 1. Helper functions to get role objects
# A function to get a role's details
def _get_role(project_id: str, role_id: int) -> dict:
    """
    Get a role's details
    
    :param project_id: str, the project ID
    :param role_id, int, the role ID
    
    :return: dict, the role's details"""
    credentials = get_credentials()
    client = iam.IAMClient(credentials=credentials)
    role_name = f'projects/{project_id}/roles/{str(role_id)}'
    print(f"Getting role: {role_name}...")
    try:
        request = iam.GetRoleRequest(name=role_name)
        response = client.get_role(request=request)
        return response
    except Exception as e:
        print(f"Failed to get role: {str(e)}")
        return None


# A function to get all roles in a project
def _get_all_roles(project_id: str) -> list:
    """
    Get all roles in a project
    
    :param project_id: str, the project ID

    :return: list, all roles in the project
    """
    credentials = get_credentials()
    client = iam.IAMClient(credentials=credentials)
    request = iam.ListRolesRequest(parent=f'projects/{project_id}')
    response = client.list_roles(request=request)
    return response.roles


# ==========================================================================
### 2. Helper functions to print given role objects
# A function to print a role's details
def _print_role(role: dict) -> None:
    """
    Print a role's details
    
    :param role: role dict(object of iam.Role), the role object
    """
    print(f'Role: {role.name}\n\nTitle: {role.title}\n\nDescription:\n{role.description}')
    print("=====================================\n")
    return


# A function to print a list of roles
def _print_roles(roles: list) -> None:
    """
    Print all roles in a project

    :param project_id: str, the project ID
    """
    print("=====================================")
    for i in range(len(roles)):
        print(f"[Role {i+1} of {len(roles)}]")
        _print_role(roles[i])
    return


# ==========================================================================
### 3. Wrapper functions to get and print role(s) in a project, using the helper functions
def print_role(project_id: str, role_id: int) -> None:
    """
    Print a role's details
    
    :param project_id: str, the project ID
    :param role_id, int, the role ID
    """
    role = _get_role(project_id, role_id)
    _print_role(role)
    return

def print_all_roles(project_id: str) -> None:
    """
    Print all roles in a project

    :param project_id: str, the project ID
    """
    roles = _get_all_roles(project_id)
    _print_roles(roles)
    return


# ==========================================================================
# Main function
if __name__ == "__main__":
    project_id = "bluese-cloudone-20200113"

    # Part 1: List all resources in a project
    print_all_roles(project_id)  # Checking if the print_all_roles function works

    
    # Part 2: Retrieve a specific resource's data
    role_title1 = "mini-collector-resource-viewer"
    role_id1 = 609

    role_title2 = "mini-collector-iam-viewer"
    role_id2 = 261

    print_role(project_id=project_id, role_id=role_id1)  # Checking if the print_role function works

    
    print("Exiting...")
    exit()


