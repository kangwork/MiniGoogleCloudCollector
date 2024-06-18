from fastapi import APIRouter
from utils.logging import get_sub_file_logger
from collectors.ce_instances import CEInstanceCollector
from utils.decorators import func_error_handler_decorator
from models.response import APIResponse
from models import request

CERouter = APIRouter(prefix="/ce", tags=["Compute Engine"])
logger = get_sub_file_logger(__name__)


# 2-4-1. A route to list all Compute Engine instances in a project
# Example use: http://localhost/ce/instances/us-west1-b
@CERouter.post("/instances", response_model=APIResponse)
@func_error_handler_decorator(logger=logger, is_api=True)
def list_ce_instances(request: request.ListResourcesRequest):
    credentials = request.credentials
    logger.add_info("list_ce_instances(): The list_ce_instances route is accessed.")
    vic = CEInstanceCollector(credentials)
    resources = vic.collect_resources()
    return {
        "data": [resource.__repr__() for resource in resources],
        "message": "List of all Compute Engine instances in the project.",
    }


# 2-4-2. A route to list all Compute Engine instances in a project in a specific zone
# Example use: http://localhost/ce/instances/us-west1-b
@CERouter.post("/instances/{zone}", response_model=APIResponse)
@func_error_handler_decorator(logger=logger, is_api=True)
def list_ce_instances_in_zone(request: request.GetResourceRequest):
    credentials, zone = request.credentials, request.param
    logger.add_info(
        f"list_ce_instances_in_zone(zone={zone}): The list_ce_instances_in_zone route is accessed."
    )
    vic = CEInstanceCollector(credentials)
    resources = vic.collect_resources_in_zone(zone)
    return {
        "data": [resource.__repr__() for resource in resources],
        "message": f"List of all Compute Engine instances in the project in {zone}.",
    }


# 2-4-3. A route to get details of a specific Compute Engine instance
@CERouter.post("/instances/{zone}/{instance_name}", response_model=APIResponse)
@func_error_handler_decorator(logger=logger, is_api=True)
# def get_ce_instance(
#     zone: str, instance_name: str, credentials=Depends(get_credentials)
# ):
def get_ce_instance(request: request.GetCEInstanceRequest):
    credentials, zone, instance_name = (
        request.credentials,
        request.zone,
        request.instance_name,
    )
    logger.add_info(
        f"get_ce_instance(zone={zone}, instance_name={instance_name}): The get_ce_instance route is accessed."
    )
    vic = CEInstanceCollector(credentials)
    resource = vic.collect_resource(zone, instance_name)
    return {
        "data": resource.__repr__(),
        "message": "Details of the specific Compute Engine instance.",
    }
