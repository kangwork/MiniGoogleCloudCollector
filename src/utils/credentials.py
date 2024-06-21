import os
from google.oauth2.service_account import Credentials
from utils.logging import get_sub_file_logger
from utils.decorators import func_error_handler_decorator
from typing import List, Dict
from utils.exceptions import CustomException
import subprocess
from datetime import datetime

logger = get_sub_file_logger(__name__)


@func_error_handler_decorator(logger=logger)
def _get_credentials_from_env() -> Credentials:
    enc_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not enc_credentials_path:
        message = "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.\n\
            Please set it to the path of the encrypted service account key file."
        logger.add_error(message)
        raise Exception(message, 401)

    if not os.path.exists(enc_credentials_path):
        message = f"There was no encrypted service information file found at {enc_credentials_path}.\n\
            Please put it under the correct mount path, or give your credentials as a dictionary."
        logger.add_error(message)
        raise Exception(message, 401)

    try:
        filename = _decrypt_file(enc_credentials_path)
        credentials = Credentials.from_service_account_file(filename)
        os.remove(filename)
    except Exception as e:
        raise Exception(
            f"Current Path: {os.getcwd()}\nCredentials Path: {enc_credentials_path}\nError: {str(e)}",
            401,
        )
    return credentials


required_fields = {
    "project_id": "",
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
def get_credentials(secret_data: Dict[str, str] = None) -> Credentials:
    if not secret_data:
        logger.add_warning(
            "Trying to get credentials from the GOOGLE_APPLICATION_CREDENTIALS environment variable."
        )
        env_credentials = _get_credentials_from_env()
        return env_credentials
    if _get_missing_fields(secret_data):
        raise CustomException(
            f"Missing required credentials fields: {_get_missing_fields(secret_data)}",
            401,
        )
    credentials = Credentials.from_service_account_info(secret_data)
    return credentials


@func_error_handler_decorator(logger=logger)
def _decrypt_file(input_path: str) -> str:
    filename = (
        f"/temp_key_files/decrypted_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    )
    encryption_key = os.getenv("ENCRYPTION_KEY")
    if not encryption_key:
        raise Exception(
            "ENCRYPTION_KEY environment variable is not set.\nPlease set it when running the container, or pass the credentials it as a dictionary.",
            401,
        )
    else:
        logger.add_info(encryption_key)
        command = [
            "gpg",
            "--quiet",
            "--batch",
            "--yes",
            "--decrypt",
            f"--passphrase={encryption_key}",
            f"--output={filename}",
            input_path,
        ]
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise Exception(
                f"Error decrypting the file.\nIt is likely that the pass phrase was incorrect. Please pass the credentials as a dictionary.",
                401,
            )
        return filename
