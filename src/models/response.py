from pydantic import BaseModel
from typing import Dict, Union, List


class APIResponse(BaseModel):
    data: dict

    def __init__(self, **data):
        super().__init__(**data)


class APIResponses(BaseModel):
    results: Union[List[APIResponse], Dict[str, List[APIResponse]]]
    total_count: int = 0

    def __init__(self, **data):
        super().__init__(**data, total_count=self.get_total_count(data))

    def get_total_count(self, values) -> int:
        results = values.get("results")
        status_code = values.get("status_code", 200)
        if status_code == 200:
            if isinstance(results, list):
                return len(results)
            elif isinstance(results, dict):
                return sum(len(v) for v in results.values())
        return 0
