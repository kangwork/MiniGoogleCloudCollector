import os
from fastapi import FastAPI
import uvicorn
from google.cloud import storage
from utils.credentials import get_credentials
from fastapi.exceptions import HTTPException
from utils.logging import Logger, setup_logger


# 1. Create a FastAPI app
app = FastAPI()

# Some other global variables
# Note that this default_project_id is just an example;
# for all the APIs, the user can specify the project ID in the URL query parameter.
# E.g. /storage/buckets?project_id=YOUR_PROJECT
logger = Logger()

def get_route_messages(default_project_id: str) -> str:
    return f"""

        Visit /storage/buckets to list all storage buckets in your project. 
        (Example: /storage/buckets?project_id={default_project_id})

        Visit /storage/buckets/BUCKET_NAME to get details of a specific storage bucket.
        (Example: /storage/buckets/mini-collector-bucket?project_id={default_project_id})
        
        """

# Example use: http://localhost/storage/buckets/airbyte_testing_001?project_id=bluese-cloudone-20200113
def list_storage_buckets(project_id: str) -> dict:
    credentials = get_credentials()

    try:
        storage_client = storage.Client(credentials=credentials, project=project_id)
        buckets = storage_client.list_buckets()
        bucket_names = [bucket.name for bucket in buckets]
        return {"buckets": bucket_names}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve buckets: {str(e)}")


# Example use: http://localhost/storage/buckets/airbyte_testing_001?project_id=bluese-cloudone-20200113
def get_storage_bucket(bucket_name: str, project_id: str) -> dict:
    credentials = get_credentials()

    try:
        storage_client = storage.Client(credentials=credentials, project=project_id)
        bucket = storage_client.get_bucket(bucket_name)

        bucket_details = {
            "name": bucket.name,
            "location": bucket.location,
            "storage_class": bucket.storage_class,
            "lifecycle_rules": bucket.lifecycle_rules,
            "labels": bucket.labels,
            "created": bucket.time_created,
        }
        return {"bucket": bucket_details}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve bucket details: {str(e)}")


# 3. Run the app
if __name__ == '__main__':
    logger = setup_logger()
    logger.add_info("This app cannot be run directly. Please run the main.py file.")
    logger.add_info("Exiting.")
    exit(0)
