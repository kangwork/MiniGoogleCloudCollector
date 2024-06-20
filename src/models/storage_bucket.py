from pydantic import BaseModel
from google.cloud.storage.client import Client
from google.cloud.storage.acl import BucketACL, DefaultObjectACL
from google.cloud.storage.bucket import Bucket
from typing import Any, Dict, Optional, Set
from pydantic import Field


class StorageBucket(BaseModel):
    """
    Model for a storage bucket
    """

    name: str
    properties: Dict[str, Any] = Field(default_factory=dict)
    changes: Set[str] = Field(default_factory=set)
    client: Optional[Client] = None
    acl: Optional[BucketACL] = None
    default_object_acl: Optional[DefaultObjectACL] = None
    label_removals: Set[str] = Field(default_factory=set)
    user_project: Optional[str] = None

    @classmethod
    def from_gcp_object(cls, obj: Bucket):
        obj = obj.__dict__

        classinstance = cls(
            name=obj["name"],
            properties=obj["_properties"],
            changes=obj["_changes"],
            client=obj["_client"],
            acl=obj["_acl"],
            default_object_acl=obj["_default_object_acl"],
            label_removals=obj["_label_removals"],
            user_project=obj["_user_project"],
        )

        return classinstance

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            BucketACL: lambda v: v.__dict__,
            DefaultObjectACL: lambda v: v.__dict__,
            Client: lambda v: v.__dict__,
        }

    def __str__(self):
        return self.name
