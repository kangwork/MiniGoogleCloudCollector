import os
from fastapi import FastAPI
import uvicorn
from google.cloud import storage
from credentials import get_credentials
from fastapi.exceptions import HTTPException
from utils.logging import Logger
from iam_roles import print_all_roles, print_role

# 1. Create a FastAPI app
app = FastAPI()

# Some other global variables
# Note that this default_project_id is just an example;
# for all the APIs, the user can specify the project ID in the URL query parameter.
# E.g. /storage/buckets?project_id=YOUR_PROJECT
default_project_id = "bluese-cloudone-20200113"


# 2. Define the routes
# 2-1. The root route
@app.get("/")
def read_root():
    return {"message": f"""Welcome to the Mini Google Cloud Collector!
            
        Note:
        The default project ID is {default_project_id}. If you want to change it, please add ?project_id=YOUR_PROJECT_ID to the URL.)
        
        Avaialable Routes:
        Visit /storage/buckets to list all storage buckets in your project. 
        (Example: /storage/buckets?project_id={default_project_id})

        Visit /storage/buckets/BUCKET_NAME to get details of a specific storage bucket.
        (Example: /storage/buckets/mini-collector-bucket?project_id={default_project_id})"""}

### 2-2. Storage Bucket APIs
# 2-2-1. A route to list all storage buckets in a project
@app.get("/storage/buckets")
def list_storage_buckets(project_id: str = default_project_id):
    credentials = get_credentials()

    try:
        storage_client = storage.Client(credentials=credentials, project=project_id)
        buckets = storage_client.list_buckets()
        bucket_names = [bucket.name for bucket in buckets]
        return {"buckets": bucket_names}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve buckets: {str(e)}")


# Example use: http://localhost/storage/buckets/airbyte_testing_001?project_id=bluese-cloudone-20200113
# 2-2-2. A route to get a storage bucket's details
@app.get("/storage/buckets/{bucket_name}")
def get_storage_bucket(bucket_name: str, project_id: str = default_project_id):
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


### 2-3. IAM Roles APIs
# 2-3-1. A route to list all IAM roles in a project
@app.get("/iam/roles")
def list_iam_roles(project_id: str = default_project_id):
    return print_all_roles(project_id, logger)

# Example use: http://localhost/iam/roles/1?project_id=bluese-cloudone-20200113
# 2-3-2. A route to get details of a specific IAM role
@app.get("/iam/roles/{role_id}")
def get_iam_role(role_id: int, project_id: str = default_project_id):
    return print_role(project_id, role_id, logger)


# # 3. Run the app
if __name__ == '__main__':
    logger = Logger("log.log")

    # Manual Deployment
    message = """
    Manual Deployment:
    The command `uvicorn get_storage_buckets:app --reload` will run the app.
    You can visit http://localhost:8000 to check the app.
    Press Ctrl+C to stop the app.
    """
    logger.add_info(message)

    # TODO: This part of the code still needs to be fixed. There's an issue with fastAPI module imports.
    # print("\nAutomatic Deployment:")
    # print("Do you want to run the app now? (y/n): ")
    # choice = input()
    # if choice == 'y':
    # OPTION 1:
    #     uvicorn.run(app, host="localhost", port=8000)
    # OPTION 2:
    #     exec_command = "uvicorn get_storage_buckets:app --reload"
    #     os.system(exec_command)
    # else:
    #     print("Exiting...")
