from pydantic import BaseModel

from app.core.mem.application.schemas.mem_read_schema import MemReadSchema


class MemReadResponse(BaseModel):
    mem: MemReadSchema
    image_bytes: bytes | None
