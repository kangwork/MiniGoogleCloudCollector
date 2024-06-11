import os
from fastapi import FastAPI, Request
from utils.logging import setup_logger, setup_main_file_logger, get_console_logger, get_sub_file_logger
from resources.storage_buckets import StorageBucketCollector
from resources.iam_roles import IAMRoleCollector
from resources.vm_instances import VMInstanceCollector
from fastapi.responses import JSONResponse
import sys
from utils.credentials import get_credentials

# A main program to call all the api functions
# =============================================================================
# 0. Setup (Create a FastAPI app, a logger, and templates)
app = FastAPI()
logger = get_sub_file_logger(__name__)
credentials = get_credentials()


# =============================================================================
# 2. APIs (Define the routes)
# 2-1. The root route
@app.get("/")
def read_root(request: Request):
    try:
        logger.add_info("read_root(): The root route is accessed.")
        message = "Welcome to the Mini Google Cloud Collector!\n\nAvailable routes:\n"
        sbc = StorageBucketCollector()
        irc = IAMRoleCollector()
        vic = VMInstanceCollector()
        message += sbc.get_route_messages()
        message += irc.get_route_messages()
        message += vic.get_route_messages()
        return {"data": "", "message": message}
    except Exception as e:
        logger.add_error(f"read_root(): {str(e)}")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the route messages."}, status_code=e.code)


### 2-2. Storage Bucket APIs
# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-1. A route to list all storage buckets in a project
@app.get("/storage/buckets")
def list_storage_buckets():
    try:
        logger.add_info("list_storage_buckets(): The list_storage_buckets route is accessed.")
        sbc = StorageBucketCollector(credentials)
        resources = sbc.collect_resources()
        simplified_resources = [str(resource) for resource in resources]
        return {"data": simplified_resources, "length": len(resources), "message": "List of all storage buckets in the project."}
    except Exception as e:
        logger.add_error("list_storage_buckets(): Failed to retrieve the storage buckets.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the storage buckets."}, status_code=e.code)
    

# Example use: http://localhost/storage/buckets/airbyte_testing_001
# 2-2-2. A route to get a storage bucket's details
@app.get("/storage/buckets/{bucket_name}")
def get_storage_bucket(bucket_name: str):
    try:
        logger.add_info(f"get_storage_bucket(bucket_name={bucket_name}): The get_storage_bucket route is accessed.")
        sbc = StorageBucketCollector(credentials)
        resource = sbc.collect_resource(bucket_name)
        return {"data": resource.__repr__(), "message": "Details of the specific storage bucket."}
    except Exception as e:
        logger.add_error(f"get_storage_bucket(bucket_name={bucket_name}): Failed to retrieve the storage bucket.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the storage bucket."}, status_code=e.code)
    

### 2-3. IAM Roles APIs
# 2-3-1. A route to list all IAM roles in a project
# Example use: http://localhost/iam/roles
@app.get("/iam/roles")
def list_iam_roles():
    try:
        logger.add_info("list_iam_roles(): The list_iam_roles route is accessed.")
        irc = IAMRoleCollector(credentials)
        resources = irc.collect_resources()
        simplified_resources = [str(resource) for resource in resources]
        return {"data": simplified_resources, "length": len(resources), "message": "List of all IAM roles in the project."}
    except Exception as e:
        logger.add_error("list_iam_roles(): Failed to retrieve the IAM roles.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the IAM roles."}, status_code=e.code)


# 2-3-2. A route to get details of a specific IAM role
# Example use: http://localhost/iam/roles/609
# Example use: http://localhost/iam/roles/261
@app.get("/iam/roles/{role_id}")
def get_iam_role(role_id: int):
    try:
        logger.add_info(f"get_iam_role(role_id={role_id}): The get_iam_role route is accessed.")
        irc = IAMRoleCollector(credentials)
        resource = irc.collect_resource(role_id)
        return {"data": resource.__repr__(), "message": "Details of the specific IAM role."}
    except Exception as e:
        logger.add_error(f"get_iam_role(role_id={role_id}): {str(e)}")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the IAM role."}, status_code=e.code)


### 2-4. VM Instances APIs
# 2-4-1. A route to list all VM instances in a project
# Example use: http://localhost/vm/instances/us-west1-b
@app.get("/vm/instances")
def list_vm_instances():
    try:
        logger.add_info("list_vm_instances(): The list_vm_instances route is accessed.")
        vic = VMInstanceCollector(credentials)
        resources = vic.collect_resources()
        simplified_resources = [str(resource) for resource in resources]
        return {"data": simplified_resources, "length": len(resources), "message": "List of all VM instances in the project."}
    except Exception as e:
        logger.add_error("list_vm_instances(): Failed to retrieve the VM instances.")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the VM instances."}, status_code=e.code)


# 2-4-2. A route to list all VM instances in a project in a specific zone
# Example use: http://localhost/vm/instances/us-west1-b
@app.get("/vm/instances/{zone}")
def list_vm_instances_in_zone(zone: str):
    try:
        logger.add_info(f"list_vm_instances_in_zone(zone={zone}): The list_vm_instances_in_zone route is accessed.")
        vic = VMInstanceCollector(credentials)
        resources = vic.collect_resources_in_zone(zone)
        simplified_resources = [str(resource) for resource in resources]
        return {"data": simplified_resources, "length": len(resources), "message": f"List of all VM instances in the project in {zone}."}
    except Exception as e:
        logger.add_error(f"list_vm_instances_in_zone(zone={zone}): Failed to retrieve the VM instances in {zone}.")
        return JSONResponse(content={"data": "", "message": f"Failed to retrieve the VM instances in {zone}."}, status_code=e.code)
    

# 2-4-3. A route to get details of a specific VM instance
@app.get("/vm/instances/{zone}/{instance_name}")
def get_vm_instance(zone: str, instance_name: str):
    try:
        logger.add_info(f"get_vm_instance(zone={zone}, instance_name={instance_name}): The get_vm_instance route is accessed.")
        vic = VMInstanceCollector(credentials)
        resource = vic.collect_resource(zone, instance_name)
        return {"data": resource.__repr__(), "message": "Details of the specific VM instance."}
    except Exception as e:
        logger.add_error(f"get_vm_instance(zone={zone}, instance_name={instance_name}): {str(e)}")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve the VM instance."}, status_code=e.code)


### 2-5. All Three at Once
# 2-5-1. A route to list all resources in a project
# Example use: http://localhost/all-resources
@app.get("/all-resources")
def list_all_resources():
    try:
        logger.add_info("list_all_resources(): The list_all_resources route is accessed.")
        sbc = StorageBucketCollector(credentials)
        irc = IAMRoleCollector(credentials)
        vic = VMInstanceCollector(credentials)
        resources = {
            "storage_buckets": sbc.collect_resources(),
            "iam_roles": irc.collect_resources(),
            "vm_instances": vic.collect_resources()
        }
        simplified_resources = {
        "storage_buckets": [str(resource) for resource in resources["storage_buckets"]],
        "iam_roles": [str(resource) for resource in resources["iam_roles"]],
        "vm_instances": [str(resource) for resource in resources["vm_instances"]]
        }
        return {"data": simplified_resources, "message": "List of all resources in the project."}
    except Exception as e:
        logger.add_error(f"list_all_resources(): {str(e)}")
        return JSONResponse(content={"data": "", "message": "Failed to retrieve all resources."}, status_code=e.code)
    

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

    os.system("uvicorn main:app --reload")