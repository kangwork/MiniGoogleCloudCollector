from google.cloud import storage
from collectors.collector import Collector
from utils.decorators import method_error_handler_decorator
from models.storage_bucket import StorageBucket
from typing import List


# =============================================================================
# Collector class
class StorageBucketCollector(Collector):
    def __init__(self, credentials=None):
        super().__init__(__name__, credentials)

    @classmethod
    def get_route_messages(self) -> str:
        route_messages = {
            "/storage/buckets": (
                "List all storage buckets in your project.",
                "/storage/buckets",
            ),
            "/storage/buckets/BUCKET_NAME": (
                "Get details of a specific storage bucket.",
                "/storage/buckets/mini-collector-bucket",
            ),
        }
        return super().get_route_messages(route_messages)

    @method_error_handler_decorator
    def collect_resources(self) -> List[StorageBucket]:
        storage_client = storage.Client(
            credentials=self.credentials, project=self.project_id
        )
        buckets = []
        for bucket in storage_client.list_buckets():
            buckets.append(StorageBucket.from_gcp_object(bucket))
        return buckets

    @method_error_handler_decorator
    def collect_resource(self, bucket_name: str) -> StorageBucket:
        storage_client = storage.Client(
            credentials=self.credentials, project=self.project_id
        )
        bucket_resource = storage_client.get_bucket(bucket_name)
        bucket = StorageBucket.from_gcp_object(bucket_resource)
        return bucket
