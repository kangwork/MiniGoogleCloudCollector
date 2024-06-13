from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from utils.logging import get_sub_file_logger
from collectors.iam_roles import IAMRoleCollector
from utils.credentials import credentials


IAMRouter = APIRouter(prefix="/iam", tags=["IAM"])
logger = get_sub_file_logger(__name__)


@IAMRouter.get("/roles")
# 2-3-1. A route to list all IAM roles in a project
# Example use: http://localhost/iam/roles
def list_iam_roles():
    try:
        logger.add_info("list_iam_roles(): The list_iam_roles route is accessed.")
        irc = IAMRoleCollector(credentials)
        resources = irc.collect_resources()
        return {
            "data": [resource.__repr__() for resource in resources],
            "length": len(resources),
            "message": "List of all IAM roles in the project.",
        }
    except Exception as e:
        logger.add_error("list_iam_roles(): Failed to retrieve the IAM roles.")
        return JSONResponse(
            content={"data": "", "message": "Failed to retrieve the IAM roles."},
            # in case there is no error code, set the status code to 500. We will use get_status_code() in the future.
            status_code=getattr(e, "code", 500),
        )


# 2-3-2. A route to get details of a specific IAM role
# Example use: http://localhost/iam/roles/609
# Example use: http://localhost/iam/roles/261
@IAMRouter.get("/roles/{role_id}")
def get_iam_role(role_id: int):
    try:
        logger.add_info(
            f"get_iam_role(role_id={role_id}): The get_iam_role route is accessed."
        )
        irc = IAMRoleCollector(credentials)
        resource = irc.collect_resource(role_id)
        return {
            "data": resource.__repr__(),
            "message": "Details of the specific IAM role.",
        }
    except Exception as e:
        logger.add_error(f"get_iam_role(role_id={role_id}): {str(e)}")
        return JSONResponse(
            content={"data": "", "message": "Failed to retrieve the IAM role."},
            status_code=getattr(e, "code", 500),
        )
