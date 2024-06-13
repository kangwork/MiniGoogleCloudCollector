from pydantic import BaseModel
from google.cloud.storage.client import Client
from google.cloud.storage.acl import BucketACL, DefaultObjectACL
from google.cloud.storage.bucket import Bucket


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

    @classmethod
    def from_gcp_object(cls, obj: Bucket):
        return cls(
            name=obj.name,
            _properties=obj._properties,
            _changes=obj._changes,
            _client=obj._client,
            _acl=obj.acl,
            _default_object_acl=obj.default_object_acl,
            _label_removals=obj._label_removals,
            _user_project=obj._user_project,
        )

    def __str__(self):
        return self.name
