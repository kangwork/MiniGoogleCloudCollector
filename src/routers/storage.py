from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils.credentials import get_credentials
from utils.logging import get_sub_file_logger
from resources.storage_buckets import StorageBucketCollector

storage = APIRouter(prefix="/storage", tags=["Storage"])
logger = get_sub_file_logger(__name__)
credentials = get_credentials()


### 2-2. Storage Bucket APIs
# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-1. A route to list all storage buckets in a project
@storage.get("/buckets")
def list_storage_buckets():
    try:
        logger.add_info(
            "list_storage_buckets(): The list_storage_buckets route is accessed."
        )
        sbc = StorageBucketCollector(credentials)
        resources = sbc.collect_resources()
        simplified_resources = [str(resource) for resource in resources]
        return {
            "data": simplified_resources,
            "length": len(resources),
            "message": "List of all storage buckets in the project.",
        }
    except Exception as e:
        logger.add_error(
            "list_storage_buckets(): Failed to retrieve the storage buckets."
        )
        return JSONResponse(
            content={"data": "", "message": "Failed to retrieve the storage buckets."},
            status_code=getattr(e, "code", 500),
        )


# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-2. A route to get a storage bucket's details
@storage.get("/buckets/{bucket_name}")
def get_storage_bucket(bucket_name: str):
    try:
        logger.add_info(
            f"get_storage_bucket(bucket_name={bucket_name}): The get_storage_bucket route is accessed."
        )
        sbc = StorageBucketCollector(credentials)
        resource = sbc.collect_resource(bucket_name)
        return {
            "data": resource.__repr__(),
            "message": "Details of the specific storage bucket.",
        }
    except Exception as e:
        logger.add_error(
            f"get_storage_bucket(bucket_name={bucket_name}): Failed to retrieve the storage bucket."
        )
        return JSONResponse(
            content={"data": "", "message": "Failed to retrieve the storage bucket."},
            status_code=getattr(e, "code", 500),
        )
