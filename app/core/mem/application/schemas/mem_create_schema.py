from pydantic import BaseModel


class MemCreateSchema(BaseModel):
    text: str
