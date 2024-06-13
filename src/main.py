import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from utils.credentials import credentials
from routers.iam import IAMRouter
from routers.storage import StorageRouter
from routers.ce import CERouter
from utils.logging import get_sub_file_logger, get_console_logger
from collectors.storage_buckets import StorageBucketCollector
from collectors.iam_roles import IAMRoleCollector
from collectors.ce_instances import CEInstanceCollector

# A main program to call all the api functions
# =============================================================================
# 0. Setup (Create a FastAPI app, a logger, and templates)
app = FastAPI()
logger = get_sub_file_logger(__name__)
# How do we make each router use the credentials value? We will pass the credentials to each router.
app.include_router(IAMRouter)
app.include_router(StorageRouter)
app.include_router(CERouter)



# =============================================================================
# 2. APIs (Define the routes)
# 2-1. The root route
@app.get("/")
def read_root(request: Request):
    try:
        logger.add_info("read_root(): The root route is accessed.")
        message = "Welcome to the Mini Google Cloud Collector!\n\nAvailable routes:\n"
        message += StorageBucketCollector.get_route_messages()
        message += IAMRoleCollector.get_route_messages()
        message += CEInstanceCollector.get_route_messages()
        return {"data": "", "message": message}
    except Exception as e:
        logger.add_error(f"read_root(): {str(e)}")
        return JSONResponse(
            content={"data": "", "message": "Failed to retrieve the route messages."},
            status_code=getattr(e, "code", 500),
        )


### 2-5. All Three at Once
# 2-5-1. A route to list all resources in a project
# Example use: http://localhost/all-resources
@app.get("/all-resources")
def list_all_resources():
    try:
        logger.add_info(
            "list_all_resources(): The list_all_resources route is accessed."
        )
        sbc = StorageBucketCollector(credentials)
        irc = IAMRoleCollector(credentials)
        cic = CEInstanceCollector(credentials)
        resources = {
            "storage_buckets": sbc.collect_resources(),
            "iam_roles": irc.collect_resources(),
            "ce_instances": cic.collect_resources(),
        }
        simplified_resources = {
            "storage_buckets": [
                str(resource) for resource in resources["storage_buckets"]
            ],
            "iam_roles": [str(resource) for resource in resources["iam_roles"]],
            "ce_instances": [str(resource) for resource in resources["ce_instances"]],
        }
        return {
            "data": simplified_resources,
            "message": "List of all resources in the project.",
        }
    except Exception as e:
        logger.add_error(f"list_all_resources(): {str(e)}")
        return JSONResponse(
            content={"data": "", "message": "Failed to retrieve all resources."},
            status_code=getattr(e, "code", 500),
        )


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
    # If the current path is MiniGoogleCloudCollector/src, the command will be executed successfully.
    # If the current path is MiniGoogleCloudCollector, the command will not be executed successfully. We need to change the path to MiniGoogleCloudCollector/src.
    # if os.getcwd().endswith("MiniGoogleCloudCollector"):
    #     os.system("uvicorn src.main:app --reload")
    # elif os.getcwd().endswith("src"):
    os.system("uvicorn main:app --reload")
    # else:
    #     console_logger.add_error(
    #         "Please change the path to MiniGoogleCloudCollector/ or MiniGoogleCloudCollector/src/ to run the app."
    #     )
    # uvicorn.run("main:app", host='0.0.0.0', port=8000, --reload)
