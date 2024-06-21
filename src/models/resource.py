from pydantic import BaseModel
from typing import List
from abc import ABC, abstractmethod


class Resource(BaseModel, ABC):

    @abstractmethod
    def from_gcp_object(cls, obj):
        pass

    def to_dict(self) -> dict:
        return self.dict()
