from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.logging import get_sub_file_logger
from collectors.storage_buckets import StorageBucketCollector
from utils.credentials import credentials
from utils.decorators import func_error_handler_decorator


StorageRouter = APIRouter(prefix="/storage", tags=["Storage"])
logger = get_sub_file_logger(__name__)


### 2-2. Storage Bucket APIs
# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-1. A route to list all storage buckets in a project
@StorageRouter.get("/buckets")
@func_error_handler_decorator(logger=logger, is_api=True)
def list_storage_buckets():
    logger.add_info(
        "list_storage_buckets(): The list_storage_buckets route is accessed."
    )
    sbc = StorageBucketCollector(credentials)
    resources = sbc.collect_resources()
    return {
        "data": [resource.__repr__() for resource in resources],
        "length": len(resources),
        "message": "List of all storage buckets in the project.",
    }


# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-2. A route to get a storage bucket's details
@StorageRouter.get("/buckets/{bucket_name}")
@func_error_handler_decorator(logger=logger, is_api=True)
def get_storage_bucket(bucket_name: str):
    logger.add_info(
        f"get_storage_bucket(bucket_name={bucket_name}): The get_storage_bucket route is accessed."
    )
    sbc = StorageBucketCollector(credentials)
    resource = sbc.collect_resource(bucket_name)
    return {
        "data": resource.__repr__(),
        "message": "Details of the specific storage bucket.",
    }
