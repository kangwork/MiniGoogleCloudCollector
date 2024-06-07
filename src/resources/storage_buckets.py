import os
from fastapi import FastAPI
import uvicorn
from google.cloud import storage
from utils.credentials import get_credentials
from fastapi.exceptions import HTTPException
from utils.logging import Logger, setup_logger


# 0. A class to represent a Storage Bucket
class StorageBucket:
    """
    A class to represent a Storage Bucket

    Attributes:
    - name: str, the bucket name
    - location: str, the bucket location
    - storage_class: str, the bucket storage class
    - lifecycle_rules: list, the bucket lifecycle rules
    - labels: dict, the bucket labels
    - created: datetime, the bucket creation time
    """
    def __init__(self, bucket: dict):
        self.name = bucket.name
        self.location = bucket.location
        self.storage_class = bucket.storage_class
        self.lifecycle_rules = bucket.lifecycle_rules
        self.labels = bucket.labels
        self.created = bucket.time_created

    def __str__(self):
        """
        Simplify the object representation for listing (bucket name)
        """
        return self.name
    



# 1. A function to return route messages
def get_route_messages(default_project_id: str) -> str:
    return f"""

        Visit /storage/buckets to list all storage buckets in your project. 
        (Example: /storage/buckets)

        Visit /storage/buckets/BUCKET_NAME to get details of a specific storage bucket.
        (Example: /storage/buckets/mini-collector-bucket)
        
        """


# =============================================================================
# 2. Helper functions to get storage bucket objects

# 2-1. A function to get storage bucket objects
def collect_resources() -> list[StorageBucket]:
    credentials = get_credentials()
    project_id = credentials.project_id

    try:
        storage_client = storage.Client(credentials=credentials, project=project_id)
        buckets = []
        for bucket in storage_client.list_buckets():
            buckets.append(StorageBucket(bucket))
        return buckets
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[{__name__}] Failed to retrieve buckets: {str(e)}")


# 2-2. A function to get a storage bucket's details
def collect_resource(bucket_name: str) -> StorageBucket:
    credentials = get_credentials()
    project_id = credentials.project_id

    try:
        storage_client = storage.Client(credentials=credentials, project=project_id)
        bucket = StorageBucket(storage_client.get_bucket(bucket_name))
        return bucket

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"[{__name__}] Failed to retrieve bucket details: {str(e)}")


# =============================================================================
# 3. Main function
if __name__ == '__main__':
    logger = Logger()
    setup_logger(logger, to_file=False)
    logger.add_info("This app cannot be run directly. Please run the main.py file.")
    logger.add_info("Exiting.")
    exit(0)
