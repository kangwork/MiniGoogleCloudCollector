from google.cloud import storage
from utils.credentials import get_credentials
from utils.logging import get_console_logger
from utils.resource import Resource
from google.cloud.storage.bucket import Bucket
from utils.collector import Collector
from utils.decorators import error_handler_decorator

# ==========================================================================
# Resource class
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
    def __init__(self, resource: Bucket):
        super().__init__(resource.__dict__)
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


# =============================================================================
# Collector class
class StorageBucketCollector(Collector):
    def __init__(self):
        super().__init__(__name__)

    def get_route_messages(self) -> str:
        route_messages = {
            "/storage/buckets": ("List all storage buckets in your project.", "/storage/buckets"),
            "/storage/buckets/BUCKET_NAME": ("Get details of a specific storage bucket.", "/storage/buckets/mini-collector-bucket")
        }
        return super().get_route_messages(route_messages)

    @error_handler_decorator
    def collect_resources(self) -> list[StorageBucket]:
        credentials = get_credentials()
        project_id = credentials.project_id
        storage_client = storage.Client(credentials=credentials, project=project_id)
        buckets = []
        for bucket in storage_client.list_buckets():
            buckets.append(StorageBucket(bucket))
        return buckets

    @error_handler_decorator
    def collect_resource(self, bucket_name: str) -> StorageBucket:
        credentials = get_credentials()
        project_id = credentials.project_id
        storage_client = storage.Client(credentials=credentials, project=project_id)
        bucket = StorageBucket(storage_client.get_bucket(bucket_name))
        return bucket


# =============================================================================
# Main function
if __name__ == '__main__':
    logger = get_console_logger()
    logger.add_warning("This app cannot be run directly. Please run the main.py file.")
    logger.add_info("Exiting.")
    exit(0)
