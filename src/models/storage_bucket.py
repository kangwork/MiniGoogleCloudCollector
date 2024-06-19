from pydantic import BaseModel
from google.cloud.storage.bucket import Bucket
from typing import Any, Dict, Optional, Set


class StorageBucket(BaseModel):
    """
    Model for a storage bucket
    """

    name: str
    properties: Dict[str, Any] = {}
    changes: Set[str] = set()
    client: str  # Client
    acl: str  # BucketACL = None
    default_object_acl: str  # DefaultObjectACL = None
    label_removals: Set[str] = set()
    user_project: Optional[str] = None

    @classmethod
    def from_gcp_object(cls, obj: Bucket):
        obj = obj.__dict__

        classinstance = cls(
            name=obj["name"],
            properties=obj["_properties"],
            changes=obj["_changes"],
            client=repr(obj["_client"]),
            acl=repr(obj["_acl"]),
            default_object_acl=repr(obj["_default_object_acl"]),
            label_removals=obj["_label_removals"],
            user_project=obj["_user_project"],
        )

        return classinstance

    class Config:
        arbitrary_types_allowed = True
