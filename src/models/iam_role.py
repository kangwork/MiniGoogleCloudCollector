from pydantic import BaseModel
from google.cloud.iam_admin_v1.types import Role as GCPIAMRole
from typing import List


class IAMRole(BaseModel):
    """
    Model for an IAM Role
    """

    name: str
    title: str
    description: str
    stage: str
    included_permissions: List[str]
    stage: GCPIAMRole.RoleLaunchStage
    etag: bytes

    @classmethod
    def from_gcp_object(cls, obj: GCPIAMRole):
        return cls(
            name=obj.name,
            title=obj.title,
            description=obj.description,
            included_permissions=obj.included_permissions,
            stage=obj.stage,
            etag=obj.etag,
        )
