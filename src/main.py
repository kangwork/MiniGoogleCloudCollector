import os
from fastapi import FastAPI, Request, Header, Depends, Body, Query
from routers.iam import IAMRouter
from routers.storage import StorageRouter
from routers.ce import CERouter
from utils.logging import get_sub_file_logger, get_console_logger
from collectors.storage_buckets import StorageBucketCollector
from collectors.iam_roles import IAMRoleCollector
from collectors.ce_instances import CEInstanceCollector
from utils.decorators import func_error_handler_decorator
from models.response import APIResponse
from google.oauth2.service_account import Credentials
from typing import Annotated

# A main program to call all the api functions
# =============================================================================
# 0. Setup (Create a FastAPI app, a logger, and templates)
app = FastAPI()
logger = get_sub_file_logger(__name__)
app.include_router(IAMRouter)
app.include_router(StorageRouter)
app.include_router(CERouter)

# =============================================================================
# 1. Credentials (Load the credentials)  --> This part will be moved to a separate module or credentials.py
# ROUGH PLANNING FOR THE CREDENTIALS RETRIEVAL VIA PARAMETERS
secret_data = {}
credential_fields = ["type", "project_id", "private_key_id", "private_key", "client_email", "client_id",
                      "auth_uri", "token_uri", "auth_provider_x509_cert_url", "client_x509_cert_url"]

def _get_missing_fields(service_account_info: dict) -> list[str]:
    logger.add_info(f"_get_missing_fields(): service_account_info: {service_account_info}")
    missing_fields = [field for field in credential_fields if field not in service_account_info]
    return missing_fields


async def _set_secret_data(service_account_info: dict = Body(...)) -> Credentials:
    credentials = Credentials.from_service_account_info(service_account_info)
    global secret_data
    secret_data["credentials"] = credentials
    return credentials


#async def get_credentials(service_account_info: Annotated[dict | None, Header()] = None) -> dict: tried and failed
async def get_credentials(service_account_info: Annotated[dict | None, Body()] = None) -> Credentials:
    if not service_account_info:
        if "credentials" not in secret_data:
            raise ValueError("No service account info is provided.", 401)
        return secret_data["credentials"]
    if _get_missing_fields(service_account_info):
        raise ValueError(f"Missing credentials fields: {_get_missing_fields(service_account_info)}", 401)
    return _set_secret_data(service_account_info)

# =============================================================================
# 2. APIs (Define the routes)
@app.post("/credentials/login", response_model=APIResponse)
@func_error_handler_decorator(logger=logger, is_api=True)
def login(service_account_info: dict = Body(...)):
    logger.add_info("login(): The set_credentials route is accessed.")
    credentials = Credentials.from_service_account_info(service_account_info)
    return {"data": "", "message": "Credentials are set."}

@app.get("/credentials/logout", response_model=APIResponse)
@func_error_handler_decorator(logger=logger, is_api=True)
def logout():
    logger.add_info("logout(): The logout route is accessed.")
    if "credentials" in secret_data:
        del secret_data["credentials"]
    return {"data": "", "message": "Credentials are removed."}


# 2-1. The root route
@app.get("/", response_model=APIResponse)
@func_error_handler_decorator(logger=logger, is_api=True)
def read_root(request: Request):
    logger.add_info("read_root(): The root route is accessed.")
    message = "Welcome to the Mini Google Cloud Collector!\n\nAvailable routes:\n"
    message += StorageBucketCollector.get_route_messages()
    message += IAMRoleCollector.get_route_messages()
    message += CEInstanceCollector.get_route_messages()
    return {"data": "", "message": message}



### 2-5. All Three at Once
# 2-5-1. A route to list all resources in a project
# Example use: http://localhost/all-resources
@app.get("/all-resources", response_model=APIResponse)
@func_error_handler_decorator(logger=logger, is_api=True)
#def list_all_resources(service_account_info: Annotated[dict | None, Header()] = None): All tried and failed
# def list_all_resources(credentials: Credentials = Depends(get_credentials)):
def list_all_resources():
    logger.add_warning(secret_data)
    credentials = secret_data["credentials"]
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
            repr(resource) for resource in resources["storage_buckets"]
        ],
        "iam_roles": [repr(resource) for resource in resources["iam_roles"]],
        "ce_instances": [repr(resource) for resource in resources["ce_instances"]],
    }
    return {
        "data": repr_resources,
        "message": "List of all resources in the project.",
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
