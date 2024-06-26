from fastapi import APIRouter
from utils.logging import get_sub_file_logger
from collectors.iam_roles import IAMRoleCollector
from utils.decorators import func_error_handler_decorator
from models.response import APIResponse, APIResponses
from models import request
from models.iam_role import IAMRole

IAMRouter = APIRouter(prefix="/iam", tags=["IAM"])
logger = get_sub_file_logger(__name__)


# 2-3-1. A route to list all IAM roles in a project
# Example use: http://localhost/iam/roles
@IAMRouter.post("/roles", response_model=APIResponses)
@func_error_handler_decorator(logger=logger, is_api=True)
def list_iam_roles(request: request.ListResourcesRequest):
    credentials = request.credentials
    logger.add_info("list_iam_roles(): The list_iam_roles route is accessed.")
    irc = IAMRoleCollector(credentials)
    resources = irc.collect_resources()
    return {"results": [APIResponse(data=dict(resource)) for resource in resources]}


# 2-3-2. A route to get details of a specific IAM role
# Example use: http://localhost/iam/roles/609
# Example use: http://localhost/iam/roles/261
@IAMRouter.post("/roles/{role_id}", response_model=APIResponse)
@func_error_handler_decorator(logger=logger, is_api=True)
def get_iam_role(request: request.GetResourceRequest):
    credentials, role_id = request.credentials, request.param
    logger.add_info(
        f"get_iam_role(role_id={role_id}): The get_iam_role route is accessed."
    )
    irc = IAMRoleCollector(credentials)
    resource = irc.collect_resource(role_id)
    return {
        "data": dict(resource),
    }
