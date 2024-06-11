from google.cloud import storage
from utils.credentials import get_credentials
from utils.logging import get_console_logger, get_sub_file_logger
from utils.resource import Resource
from google.cloud.storage.bucket import Bucket

logger = get_sub_file_logger(__name__)

# 0. A class to represent a Storage Bucket
class StorageBucket(Resource):
    """
    A class to represent a Storage Bucket

    Attributes:
    - name: str, the bucket name
    - location: str, the bucket location
    - storage_class: str, the bucket storage class
    - lifecycle_rules: list, the bucket lifecycle rules
    - labels: dict, the bucket labels
    - created: datetime, the bucket creation time
    """
    def __init__(self, resource: Bucket = None):
        super().__init__()
        self.name = None
        self.location = None
        self.storage_class = None
        self.lifecycle_rules = None
        self.labels = None
        self.created = None
        if resource:
            self.set_resource(resource)

    def set_resource(self, resource: dict):
        super().set_resource(resource.__dict__)
        self.name = resource.name
        self.location = resource.location
        self.storage_class = resource.storage_class
        self.lifecycle_rules = resource.lifecycle_rules
        self.labels = resource.labels
        self.created = resource.time_created

    def __str__(self):
        """
        Simplify the object representation for listing (bucket name)
        """
        return self.name
    
    # 1. A function to return route messages
    def get_route_messages(self) -> str:
        return """

            Visit /storage/buckets to list all storage buckets in your project. 
            (Example: /storage/buckets)

            Visit /storage/buckets/BUCKET_NAME to get details of a specific storage bucket.
            (Example: /storage/buckets/mini-collector-bucket)
            
            """


# =============================================================================
# 2. Helper functions to get storage bucket objects

# 2-1. A function to get storage bucket objects
def collect_resources() -> list[StorageBucket] | int:
    credentials = get_credentials()
    project_id = credentials.project_id

    try:
        storage_client = storage.Client(credentials=credentials, project=project_id)
        buckets = []
        for bucket in storage_client.list_buckets():
            buckets.append(StorageBucket(bucket))
        return buckets
    
    except Exception as e:
        logger.add_error(f"collect_resources(): {str(e)}")
        return e.code

# 2-2. A function to get a storage bucket's details
def collect_resource(bucket_name: str) -> StorageBucket | int:
    credentials = get_credentials()
    project_id = credentials.project_id

    try:
        storage_client = storage.Client(credentials=credentials, project=project_id)
        bucket = StorageBucket(storage_client.get_bucket(bucket_name))
        return bucket

    except Exception as e:
        logger.add_error(f"collect_resource(bucket_name={bucket_name}): {str(e)}")
        return e.code


# =============================================================================
# 3. Main function
if __name__ == '__main__':
    logger = get_console_logger()
    logger.add_warning("This app cannot be run directly. Please run the main.py file.")
    logger.add_info("Exiting.")
    exit(0)
