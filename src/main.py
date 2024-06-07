import os
from fastapi import FastAPI, Request
import uvicorn
from google.cloud import storage
from utils.credentials import get_credentials
from fastapi.exceptions import HTTPException
from utils.logging import Logger, setup_logger
from resources import storage_buckets, iam_roles, vm_instances
from fastapi.responses import JSONResponse
import json
from fastapi.templating import Jinja2Templates


# A main program to call all the api functions

# =============================================================================
# 0. Setup (Create a FastAPI app, a logger, and templates)
app = FastAPI()
templates = Jinja2Templates(directory="../templates")
logger = Logger()


# =============================================================================
# 2. APIs (Define the routes)
# 2-1. The root route
@app.get("/")
def read_root(request: Request):
    default_project_id = "YOUR_PROJECT_ID_HERE"

    message = f"""Welcome to the Mini Google Cloud Collector!
    
        Avaialable Routes:
        """
    
    message += storage_buckets.get_route_messages(default_project_id)
    message += iam_roles.get_route_messages(default_project_id)
    message += vm_instances.get_route_messages(default_project_id)
    json_data = json.dumps({"message": message}, indent=4, sort_keys=True)
    return templates.TemplateResponse("template.html", {"request": request, "json_data": json_data})
    # return {"data": message}


### 2-2. Storage Bucket APIs
# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-1. A route to list all storage buckets in a project
@app.get("/storage/buckets")
def list_storage_buckets():
    resources = storage_buckets.collect_resources() 
    simplified_resources = [str(resource) for resource in resources]
    return {"data": simplified_resources, "length": len(message), "message": "List of all storage buckets in the project."}


# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-2. A route to get a storage bucket's details
@app.get("/storage/buckets/{bucket_name}")
def get_storage_bucket(bucket_name: str):
    resource = storage_buckets.collect_resource(bucket_name) 
    return {"data": resource, "message": "Details of the specific storage bucket."}


### 2-3. IAM Roles APIs
# 2-3-1. A route to list all IAM roles in a project
# Example use: http://localhost/iam/roles
@app.get("/iam/roles")
def list_iam_roles():
    resources = iam_roles.collect_resources(logger)
    simplified_resources = [str(resource) for resource in resources]
    return {"data": simplified_resources, "length": len(resources), "message": "List of all IAM roles in the project."}


# Example use: http://localhost/iam/roles/609
# Example use: http://localhost/iam/roles/261
# 2-3-2. A route to get details of a specific IAM role
@app.get("/iam/roles/{role_id}")
def get_iam_role(role_id: int):
    resource = iam_roles.collect_resource(role_id, logger)
    return {"data": resource, "message": "Details of the specific IAM role."}


### 2-4. VM Instances APIs
# 2-4-1. A route to list all VM instances in a project
# Example use: http://localhost/vm/instances/us-west1-b
@app.get("/vm/instances/{zone}")
def list_vm_instances():
    resources = vm_instances.collect_resources() 
    simplified_resources = [str(resource) for resource in resources]
    return {"data": simplified_resources, "length": len(resources), "message": "List of all VM instances in the project."}


# Example use: http://localhost/vm/instances/us-west1-b/mini-collector-instance
# 2-4-2. A route to get details of a specific VM instance
@app.get("/vm/instances/{zone}/{instance_name}")
def get_vm_instance(zone: str, instance_name: str):
    resource = vm_instances.collect_resource(zone, instance_name)
    return {"data": resource, "message": "Details of the specific VM instance."}


# =============================================================================
# 3. Main function (Run the app)
if __name__ == '__main__':
    # Ask the user if they want to log the output in a file
    print("Do you want to log the output in a file? (y/n):")
    choice = input()
    if choice.lower() == 'y':
        # Clear the log file
        with open("log.log", "w") as f:
            f.write("")
        setup_logger(logger, to_file=True)
    else:
        logger = setup_logger(False)

    message = """
    The Mini Google Cloud Collector is running!
    - The command `uvicorn main:app --reload` will be executed by the script.
    - You can visit http://localhost:8000 to check the app.
    - Press Ctrl+C to stop the app.
    """
    logger.add_info(message)
    os.system("uvicorn main:app --reload")