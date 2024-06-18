from pydantic import BaseModel
from typing import Dict
from utils.credentials import get_credentials
from abc import ABC

# class SecretData(BaseModel): I don't know if it is better to define this class, so I will leave it till the meeting today.
#     private_key: str
#     client_email: str
#     project_id: str = None

#     @property
#     def credentials(self):
#         return get_credentials(self.dict())

class ResourceAccessRequest(BaseModel, ABC):
    secret_data: Dict[str, str]

    @property
    def credentials(self):
        return get_credentials(self.secret_data)


class ListResourcesRequest(ResourceAccessRequest):
    pass


class GetResourceRequest(ResourceAccessRequest):
    param: str  # role_id, bucket_name, etc


class GetCEInstanceRequest(ResourceAccessRequest):
    zone: str
    instance_name: str
