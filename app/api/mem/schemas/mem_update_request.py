from pydantic import BaseModel


class MemUpdateRequest(BaseModel):
    text: str
