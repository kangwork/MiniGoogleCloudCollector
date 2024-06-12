from pydantic import BaseModel
from google.cloud.storage.client import Client
from google.cloud.storage.acl import BucketACL, DefaultObjectACL


class StorageBucket(BaseModel):
    """
    Model for a storage bucket
    """
    name: str
    _properties: dict
    _changes: set
    _client: Client
    _acl: BucketACL
    _default_object_acl: DefaultObjectACL
    _label_removals: set
    _user_project: object  # None