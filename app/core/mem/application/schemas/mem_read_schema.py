from uuid import UUID

from pydantic import BaseModel

from app.core.mem.domain.mem_entity import Mem


class MemReadSchema(BaseModel):
    uuid: UUID
    text: str

    @classmethod
    def from_entity(cls, entity: Mem) -> "MemReadSchema":
        return cls(
            uuid=entity.uuid.uuid,
            text=entity.text.text
        )
