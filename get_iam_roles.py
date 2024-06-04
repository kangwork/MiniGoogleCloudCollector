from google.cloud import iam
from credentials import get_credentials

# 지금 패키지 문제 때문에 안 돌아갑니다. 집에 가서 다시 보고 싶기 때문에 커밋합니다!

# A function to get a role's details
def _get_role(project_id: str, role_name: str) -> dict:
    """
    Get a role's details
    
    :param project_id: str, the project ID
    :param role_name: str, the role name
    
    :return: dict, the role's details"""
    credentials = get_credentials()
    client = iam.v1.IAMClient(credentials=credentials)
    request = iam.GetRoleRequest(name=f'projects/{project_id}/roles/{role_name}')
    response = client.get_role(request=request)
    return response


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

# A function to print a role's details
def print_role(project_id: str, role_name: str) -> None:
    """
    Print a role's details
    
    :param project_id: str, the project ID
    :param role_name: str, the role name
    """
    role = _get_role(project_id, role_name)
    print(f'Role: {role.name}, Title: {role.title}, Description: {role.description}')
    return


# A function to print all roles in a project
def print_all_roles(project_id: str) -> None:
    """
    Print all roles in a project

    :param project_id: str, the project ID
    """
    roles = _get_all_roles(project_id)
    for role in roles:
        print_role(role)
    return



if __name__ == "__main__":
    project_id = "bluese-cloudone-20200113"

    # Part 1: Retrieve a specific resource's data
    role_name = "roles/compute.instanceAdmin"
    print_role(project_id, role_name)  # Checking if the print_role function works

    # Part 2: List all resources in a project
    print_all_roles(project_id)  # Checking if the print_all_roles function works

    print("Exiting...")
    exit()

