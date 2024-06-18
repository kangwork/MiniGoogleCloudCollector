import os
from google.oauth2.service_account import Credentials
from utils.logging import get_sub_file_logger
from utils.decorators import func_error_handler_decorator
from typing_extensions import Annotated
from fastapi import Body
from typing import List, Union

logger = get_sub_file_logger(__name__)


@func_error_handler_decorator(logger=logger)
def _get_credentials_from_env() -> Credentials:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not credentials_path:
        message = """GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.\nPlease set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your credentials file.\nE.g. export GOOGLE_APPLICATION_CREDENTIALS='../local/mini-collector/key.json'"""
        logger.add_error(message)
        raise Exception(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.", 401
        )

    try:
        credentials = Credentials.from_service_account_file(credentials_path)

    except Exception as e:
        raise Exception(
            f"Current Path: {os.getcwd()}\nCredentials Path: {credentials_path}\nError: {str(e)}",
            401,
        )
    return credentials


required_fields = {
    "private_key": "",
    "client_email": "",
    "token_uri": "https://oauth2.googleapis.com/token",
    "universe_domain": "googleapis.com",
}


@func_error_handler_decorator(logger=logger)
def _get_missing_fields(service_account_info: dict) -> List[str]:
    missing_required_fields = []
    for field in required_fields:
        if field not in service_account_info:
            default_value = required_fields[field]
            if default_value:
                logger.add_warning(
                    f"Using default value for missing field ({field}={default_value})"
                )
                service_account_info[field] = default_value
            else:
                missing_required_fields.append(field)
    return missing_required_fields


@func_error_handler_decorator(logger=logger)
def get_credentials(
    input_dict: Annotated[Union[dict, None], Body()] = None
) -> Credentials:
    if not input_dict:
        logger.add_warning("No input dictionary is provided.")
    else:
        secret_data = input_dict.get("secret_data")
        if not secret_data:
            logger.add_warning(
                "No secret_data field is provided in the input dictionary."
            )
    if not input_dict or not secret_data:
        logger.add_warning(
            "Trying to get credentials from the GOOGLE_APPLICATION_CREDENTIALS environment variable."
        )
        env_credentials = _get_credentials_from_env()
        return env_credentials
    if _get_missing_fields(secret_data):
        raise ValueError(
            f"Missing required credentials fields: {_get_missing_fields(secret_data)}",
            401,
        )
    credentials = Credentials.from_service_account_info(secret_data)
    return credentials
