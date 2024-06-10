import os
import json
from google import oauth2
from utils.logging import get_sub_file_logger

# A function to get credentials.
def get_credentials():
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    if not credentials_path:
        logger = get_sub_file_logger(__name__)
        message = """GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.\nPlease set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your credentials file.\nE.g. export GOOGLE_APPLICATION_CREDENTIALS='../local/mini-collector/key.json'"""
        logger.add_error(message)
        raise Exception("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
    
    credentials = oauth2.service_account.Credentials.from_service_account_file(credentials_path)
    return credentials