import os
from fastapi import FastAPI
from routers.iam import IAMRouter
from routers.storage import StorageRouter
from routers.ce import CERouter
from utils.logging import get_sub_file_logger, get_console_logger
from collectors.storage_buckets import StorageBucketCollector
from collectors.iam_roles import IAMRoleCollector
from collectors.ce_instances import CEInstanceCollector
from utils.decorators import func_error_handler_decorator
from models.response import APIResponse, APIResponses
from models import request

# A main program to call all the api functions
# =============================================================================
# 0. Setup (Create a FastAPI app, a logger, and templates)
app = FastAPI()
logger = get_sub_file_logger(__name__)
app.include_router(IAMRouter)
app.include_router(StorageRouter)
app.include_router(CERouter)


# =============================================================================
# 2. APIs (Define the routes)
# 2-1. The root route
@app.get("/", response_model=APIResponse)
@func_error_handler_decorator(logger=logger, is_api=True)
def read_root():
    logger.add_info("read_root(): The root route is accessed.")
    data = {}
    data["heading"] = (
        "Welcome to the Mini Google Cloud Collector!\n\nAvailable routes:\n"
    )
    data["storage_buckets"] = StorageBucketCollector.get_route_messages()
    data["iam_roles"] = IAMRoleCollector.get_route_messages()
    data["ce_instances"] = CEInstanceCollector.get_route_messages()
    return {"data": data}


### 2-5. All Three at Once
# 2-5-1. A route to list all resources in a project
# Example use: http://localhost/all-resources
@app.post("/all-resources", response_model=APIResponses)
@func_error_handler_decorator(logger=logger, is_api=True)
def list_all_resources(request: request.ListResourcesRequest):
    credentials = request.credentials
    logger.add_info("list_all_resources(): The list_all_resources route is accessed.")
    sbc = StorageBucketCollector(credentials)
    irc = IAMRoleCollector(credentials)
    cic = CEInstanceCollector(credentials)
    resources = {
        "storage_buckets": sbc.collect_resources(),
        "iam_roles": irc.collect_resources(),
        "ce_instances": cic.collect_resources(),
    }
    repr_resources = {
        "storage_buckets": [
            APIResponse(data=dict(resource))
            for resource in resources["storage_buckets"]
        ],
        "iam_roles": [
            APIResponse(data=dict(resource)) for resource in resources["iam_roles"]
        ],
        "ce_instances": [
            APIResponse(data=dict(resource)) for resource in resources["ce_instances"]
        ],
    }
    return {
        "results": repr_resources,
    }


# =============================================================================
# 3. Main function (Run the app)
if __name__ == "__main__":

    console_logger = get_console_logger(__name__)
    instruction = """
    The Mini Google Cloud Collector is running!
    - The command `uvicorn main:app --reload` will be executed by the script.
    - You can visit http://localhost:8000 to check the app.
    - Press Ctrl+C to stop the app.
    """
    console_logger.add_info(instruction)
    os.system("uvicorn main:app --reload")
