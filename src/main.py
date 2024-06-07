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


# A main function to call all the api functios
# 1. Create a FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="../templates")

# Some other global variables
# Note that this default_project_id is just an example;
# for all the APIs, the user can specify the project ID in the URL query parameter.
# E.g. /storage/buckets?project_id=YOUR_PROJECT
default_project_id = "bluese-cloudone-20200113"
logger = Logger()

# 2. Define the routes
# 2-1. The root route
@app.get("/")
def read_root(request: Request):

    message = f"""Welcome to the Mini Google Cloud Collector!
            
        Note:
        The default project ID is {default_project_id}. 
        If you want to change it, please add ?project_id=YOUR_PROJECT_ID to the URL.)
        
        Avaialable Routes:
        """
    
    message += storage_buckets.get_route_messages(default_project_id)
    message += iam_roles.get_route_messages(default_project_id)
    message += vm_instances.get_route_messages(default_project_id)
    json_data = json.dumps({"message": message}, indent=4, sort_keys=True)
    return templates.TemplateResponse("template.html", {"request": request, "json_data": json_data})
    # return {"message": message}


### 2-2. Storage Bucket APIs
# Example use: http://localhost/storage/buckets/airbyte_testing_001?project_id=bluese-cloudone-20200113
# 2-2-1. A route to list all storage buckets in a project
@app.get("/storage/buckets")
def list_storage_buckets():
    message = storage_buckets.list_storage_buckets()
    return {"buckets": message}


# Example use: http://localhost/storage/buckets/airbyte_testing_001?project_id=bluese-cloudone-20200113
# 2-2-2. A route to get a storage bucket's details
@app.get("/storage/buckets/{bucket_name}")
def get_storage_bucket(bucket_name: str):
    message = storage_buckets.get_storage_bucket(bucket_name)
    return {"bucket": message}


### 2-3. IAM Roles APIs
# 2-3-1. A route to list all IAM roles in a project
# Example use: http://localhost/iam/roles?project_id=bluese-cloudone-20200113
@app.get("/iam/roles")
def list_iam_roles():
    message = iam_roles.print_all_roles(logger)
    return {"roles": message}


# Example use: http://localhost/iam/roles/609?project_id=bluese-cloudone-20200113
# Example use: http://localhost/iam/roles/261
# 2-3-2. A route to get details of a specific IAM role
@app.get("/iam/roles/{role_id}")
def get_iam_role(role_id: int):
    message = iam_roles.print_role(role_id, logger)
    return {"role": message}


### 2-4. VM Instances APIs
# 2-4-1. A route to list all VM instances in a project
# Example use: http://localhost/vm/instances?project_id=bluese-cloudone-20200113
@app.get("/vm/instances")
def list_vm_instances(project_id: str = default_project_id):
    message = vm_instances.list_instances(project_id)
    return {"instances": message}


# Example use: http://localhost/vm/instances/us-west1-b/mini-collector-instance?project_id=bluese-cloudone-20200113
# 2-4-2. A route to get details of a specific VM instance
@app.get("/vm/instances/{zone}/{instance_name}")
def get_vm_instance(zone: str, instance_name: str):
    message = vm_instances.get_instance_details(project_id, zone, instance_name)
    return {"instance": message}

# 3. Run the app
if __name__ == '__main__':


    # This logger refers to the global logger
    print("Do you want to log the output in a file? (y/n):")
    choice = input()
    if choice.lower() == 'y':
        # Clear the log file
        with open("log.log", "w") as f:
            f.write("")
        setup_logger(logger, to_file=True)
    else:
        logger = setup_logger(False)

    # Manual Deployment
    message = """
    Manual Deployment:
    - The command `uvicorn main:app --reload` will be executed.
    - You can visit http://localhost:8000 to check the app.
    - Press Ctrl+C to stop the app.
    """
    logger.add_info(message)

    # On the terminal, run the command: `uvicorn main:app --reload`
    # Execute it in the terminal to run the app, while not CTRL+C to stop it.
    # The app will be available at http://localhost:8000

    os.system("uvicorn main:app --reload")


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
