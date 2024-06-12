from pydantic import BaseModel
from google.cloud.iam_admin_v1.types import Role as GCPIAMRole



class IAMRole(BaseModel):
    """
    Model for an IAM Role
    """

    name: str
    title: str
    description: str
    stage: str
    included_permissions: list[str]
    stage: GCPIAMRole.RoleLaunchStage
    etag: bytes


    @classmethod
    def from_gcp_resource(cls, role: GCPIAMRole):
        return cls(
            name=role.name,
            title=role.title,
            description=role.description,
            included_permissions=role.included_permissions,
            stage=role.stage,
            etag=role.etag,
        )
