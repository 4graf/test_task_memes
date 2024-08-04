from uuid import UUID

from pydantic import BaseModel

from app.core.mem.domain.mem_entity import Mem


class MemReadSchema(BaseModel):
    uuid: UUID
    text: str
    image_path: str | None

    @classmethod
    def from_entity(cls, entity: Mem) -> "MemReadSchema":
        image_path = entity.image_path.path if entity.image_path else None
        return cls(
            uuid=entity.uuid.uuid,
            text=entity.text.text,
            image_path=image_path
        )
