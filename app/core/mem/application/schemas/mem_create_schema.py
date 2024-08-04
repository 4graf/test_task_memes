from pydantic import BaseModel


class MemCreateSchema(BaseModel):
    text: str
    # image_path: str | None
