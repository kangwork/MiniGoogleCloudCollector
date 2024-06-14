from pydantic import BaseModel


class APIResponse(BaseModel):
    data: str | list | dict[str, list]
    length: int = -1
    status_code: int = 200
    message: str = "Thanks for using the Mini Google Cloud Collector."

    def __init__(self, **data):
        super().__init__(**data, length=self.get_length(data, data))

    def get_length(cls, v, values) -> int:
        data = values.get("data")
        status_code = values.get("status_code", 200)
        if status_code == 200:
            if isinstance(data, list):
                return len(data)
            elif isinstance(data, dict):
                return sum(len(v) for v in data.values())
            elif isinstance(data, str):
                return 1
        return 0

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "data": "",
                "length": 0,
                "status_code": 200,
                "message": "List of all resources in the project.",
            }
        }
