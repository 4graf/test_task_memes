from uuid import UUID

from pydantic import BaseModel


class MemUpdateSchema(BaseModel):
    uuid: UUID
    text: str
    image_path: str | None
