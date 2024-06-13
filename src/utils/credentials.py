import os
from google.oauth2.service_account import Credentials
from utils.logging import get_sub_file_logger

# A function to get credentials.
def get_credentials() -> Credentials:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not credentials_path:
        logger = get_sub_file_logger(__name__)
        message = """GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.\nPlease set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your credentials file.\nE.g. export GOOGLE_APPLICATION_CREDENTIALS='../local/mini-collector/key.json'"""
        logger.add_error(message)
        raise Exception(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is not set."
        )

    try:
        credentials = Credentials.from_service_account_file(credentials_path)

    except Exception as e:
        raise Exception(
            f"Current Path: {os.getcwd()}\nCredentials Path: {credentials_path}\nError: {str(e)}"
        )
    return credentials

credentials = get_credentials()