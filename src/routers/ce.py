from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.logging import get_sub_file_logger
from collectors.ce_instances import CEInstanceCollector
from utils.credentials import credentials

CERouter = APIRouter(prefix="/ce", tags=["Compute Engine"])
logger = get_sub_file_logger(__name__)


# 2-4-1. A route to list all Compute Engine instances in a project
# Example use: http://localhost/ce/instances/us-west1-b
@CERouter.get("/instances")
def list_ce_instances():
    try:
        logger.add_info("list_ce_instances(): The list_ce_instances route is accessed.")
        vic = CEInstanceCollector(credentials)
        resources = vic.collect_resources()
        return {
            "data": [resource.__repr__() for resource in resources],
            "length": len(resources),
            "message": "List of all Compute Engine instances in the project.",
        }
    except Exception as e:
        logger.add_error(
            "list_ce_instances(): Failed to retrieve the Compute Engine instances."
        )
        return JSONResponse(
            content={
                "data": "",
                "message": "Failed to retrieve the Compute Engine instances.",
            },
            status_code=getattr(e, "code", 500),
        )


# 2-4-2. A route to list all Compute Engine instances in a project in a specific zone
# Example use: http://localhost/ce/instances/us-west1-b
@CERouter.get("/instances/{zone}")
def list_ce_instances_in_zone(zone: str):
    try:
        logger.add_info(
            f"list_ce_instances_in_zone(zone={zone}): The list_ce_instances_in_zone route is accessed."
        )
        vic = CEInstanceCollector(credentials)
        resources = vic.collect_resources_in_zone(zone)
        return {
            "data": [resource.__repr__() for resource in resources],
            "length": len(resources),
            "message": f"List of all Compute Engine instances in the project in {zone}.",
        }
    except Exception as e:
        logger.add_error(
            f"list_ce_instances_in_zone(zone={zone}): Failed to retrieve the Compute Engine instances in {zone}."
        )
        return JSONResponse(
            content={
                "data": "",
                "message": f"Failed to retrieve the Compute Engine instances in {zone}.",
            },
            status_code=getattr(e, "code", 500),
        )


# 2-4-3. A route to get details of a specific Compute Engine instance
@CERouter.get("/instances/{zone}/{instance_name}")
def get_ce_instance(zone: str, instance_name: str):
    try:
        logger.add_info(
            f"get_ce_instance(zone={zone}, instance_name={instance_name}): The get_ce_instance route is accessed."
        )
        vic = CEInstanceCollector(credentials)
        resource = vic.collect_resource(zone, instance_name)
        return {
            "data": resource.__repr__(),
            "message": "Details of the specific Compute Engine instance.",
        }
    except Exception as e:
        logger.add_error(
            f"get_ce_instance(zone={zone}, instance_name={instance_name}): {str(e)}"
        )
        return JSONResponse(
            content={
                "data": "",
                "message": "Failed to retrieve the Compute Engine instance.",
            },
            status_code=getattr(e, "code", 500),
        )
