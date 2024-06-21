from pydantic import BaseModel
from typing import Dict
from utils.credentials import get_credentials
from abc import ABC


class ResourceAccessRequest(BaseModel, ABC):
    secret_data: Dict[str, str]

    @property
    def credentials(self):
        return get_credentials(self.secret_data)


class ListResourcesRequest(ResourceAccessRequest):
    pass


class GetResourceRequest(ResourceAccessRequest):
    param: str


class GetCEInstanceRequest(ResourceAccessRequest):
    zone: str
    instance_name: str
