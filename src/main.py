import os
from fastapi import FastAPI, Request
from utils.logging import setup_logger, setup_main_file_logger, get_console_logger, get_sub_file_logger
from resources import storage_buckets, iam_roles, vm_instances
from resources.storage_buckets import StorageBucketCollector
from resources.iam_roles import IAMRoleCollector
from resources.vm_instances import VMInstanceCollector
from fastapi.responses import JSONResponse
import sys


# A main program to call all the api functions

# =============================================================================
# 0. Setup (Create a FastAPI app, a logger, and templates)
app = FastAPI()
logger = get_sub_file_logger(__name__)


# =============================================================================
# 2. APIs (Define the routes)
# 2-1. The root route
@app.get("/")
def read_root(request: Request):
    logger.add_info("read_root(): The root route is accessed.")

    message = """Welcome to the Mini Google Cloud Collector!
    
        Avaialable Routes:
        """
    try:
        sbc = StorageBucketCollector()
        irc = IAMRoleCollector()
        vic = VMInstanceCollector()
        message += sbc.get_route_messages()
        message += irc.get_route_messages()
        message += vic.get_route_messages()
        return {"data": "", "message": message}
    except Exception as e:
        logger.add_error(f"read_root(): {str(e)}")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the route messages."}, status_code=500)


### 2-2. Storage Bucket APIs
# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-1. A route to list all storage buckets in a project
@app.get("/storage/buckets")
def list_storage_buckets():
    logger.add_info("list_storage_buckets(): The list_storage_buckets route is accessed.")
    resources = storage_buckets.collect_resources() 
    if isinstance(resources, int):
        logger.add_error("list_storage_buckets(): Failed to retrieve the storage buckets.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the storage buckets."}, status_code=resources)
    simplified_resources = [str(resource) for resource in resources]
    return {"data": simplified_resources, "length": len(resources), "message": "List of all storage buckets in the project."}


# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-2. A route to get a storage bucket's details
@app.get("/storage/buckets/{bucket_name}")
def get_storage_bucket(bucket_name: str):
    logger.add_info(f"get_storage_bucket(bucket_name={bucket_name}): The get_storage_bucket route is accessed.")
    resource = storage_buckets.collect_resource(bucket_name)
    if isinstance(resource, int):
        logger.add_error(f"get_storage_bucket(bucket_name={bucket_name}): Failed to retrieve the storage bucket.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the storage bucket."}, status_code=resource)
    return {"data": resource.__repr__(), "message": "Details of the specific storage bucket."}


### 2-3. IAM Roles APIs
# 2-3-1. A route to list all IAM roles in a project
# Example use: http://localhost/iam/roles
@app.get("/iam/roles")
def list_iam_roles():
    logger.add_info("list_iam_roles(): The list_iam_roles route is accessed.")
    resources = iam_roles.collect_resources()
    if isinstance(resources, int):
        logger.add_error("list_iam_roles(): Failed to retrieve the IAM roles.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the IAM roles."}, status_code=resources)
    simplified_resources = [str(resource) for resource in resources]
    return {"data": simplified_resources, "length": len(resources), "message": "List of all IAM roles in the project."}


# Example use: http://localhost/iam/roles/609
# Example use: http://localhost/iam/roles/261
# 2-3-2. A route to get details of a specific IAM role
@app.get("/iam/roles/{role_id}")
def get_iam_role(role_id: int):
    logger.add_info(f"get_iam_role(role_id={role_id}): The get_iam_role route is accessed.")
    resource = iam_roles.collect_resource(role_id)
    if isinstance(resource, int):
        logger.add_error(f"get_iam_role(role_id={role_id}): Failed to retrieve the IAM role.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the IAM role."}, status_code=resource)
    return {"data": resource.__repr__(), "message": "Details of the specific IAM role."}


### 2-4. VM Instances APIs
# 2-4-1. A route to list all VM instances in a project
# Example use: http://localhost/vm/instances/us-west1-b
@app.get("/vm/instances")
def list_vm_instances():
    logger.add_info("list_vm_instances(): The list_vm_instances route is accessed.")
    resources = vm_instances.collect_resources()
    if isinstance(resources, int):
        logger.add_error("list_vm_instances(): Failed to retrieve the VM instances.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the VM instances."}, status_code=resources)
    simplified_resources = [str(resource) for resource in resources]
    return {"data": simplified_resources, "length": len(resources), "message": "List of all VM instances in the project."}


# 2-4-2. A route to list all VM instances in a project in a specific zone
# Example use: http://localhost/vm/instances/us-west1-b
@app.get("/vm/instances/{zone}")
def list_vm_instances_in_zone(zone: str):
    logger.add_info(f"list_vm_instances_in_zone(zone={zone}): The list_vm_instances_in_zone route is accessed.")
    resources = vm_instances.collect_resources_in_zone(zone)
    if isinstance(resources, int):
        logger.add_error(f"list_vm_instances_in_zone(zone={zone}): Failed to retrieve the VM instances in {zone}.")
        return JSONResponse(content={"data": "", "message": f"Failed to retrieve the VM instances in {zone}."}, status_code=resources)
    simplified_resources = [str(resource) for resource in resources]
    return {"data": simplified_resources, "length": len(resources), "message": f"List of all VM instances in the project in {zone}."}



# Example use: http://localhost/vm/instances/us-west1-b/mini-collector-instance
# 2-4-3. A route to get details of a specific VM instance
@app.get("/vm/instances/{zone}/{instance_name}")
def get_vm_instance(zone: str, instance_name: str):
    logger.add_info(f"get_vm_instance(zone={zone}, instance_name={instance_name}): The get_vm_instance route is accessed.")
    resource = vm_instances.collect_resource(zone, instance_name)
    if isinstance(resource, int):
        logger.add_error(f"get_vm_instance(zone={zone}, instance_name={instance_name}): Failed to retrieve the VM instance.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the VM instance."}, status_code=resource)
    return {"data": resource.__repr__(), "message": "Details of the specific VM instance."}


# =============================================================================
# 3. Main function (Run the app)
if __name__ == '__main__':
    
    console_logger = get_console_logger(__name__)
    instruction = """
    The Mini Google Cloud Collector is running!
    - The command `uvicorn main:app --reload` will be executed by the script.
    - You can visit http://localhost:8000 to check the app.
    - Press Ctrl+C to stop the app.
    """
    console_logger.add_info(instruction)

    # If the first argument is not 'y', we will ask a user if they want to log the output in a file
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'y':
        setup_main_file_logger(logger)
    else:
        print("Do you want to log the output in a file? (y/n):")
        choice = input()
        if choice.lower() == 'n':
            setup_logger(logger, False)
    
    os.system("uvicorn main:app --reload")