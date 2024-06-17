import os
from google.oauth2.service_account import Credentials
from utils.logging import get_sub_file_logger
from utils.decorators import func_error_handler_decorator
from typing import Annotated
from fastapi import Body

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


credential_fields = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "auth_uri",
    "token_uri",
    "auth_provider_x509_cert_url",
    "client_x509_cert_url",
]


@func_error_handler_decorator(logger=logger)
def _get_missing_fields(service_account_info: dict) -> list[str]:
    missing_fields = [
        field for field in credential_fields if field not in service_account_info
    ]
    return missing_fields


@func_error_handler_decorator(logger=logger)
def get_credentials(
    service_account_info: Annotated[dict | None, Body()] = None
) -> Credentials:
    if not service_account_info:
        logger.add_warning(
            "No service account info is provided; using GOOGLE_APPLICATION_CREDENTIALS from the environment."
        )
        env_credentials = _get_credentials_from_env()
        return env_credentials
    if _get_missing_fields(service_account_info):
        raise ValueError(
            f"Missing credentials fields: {_get_missing_fields(service_account_info)}",
            401,
        )
    credentials = Credentials.from_service_account_info(service_account_info)
    return credentials
