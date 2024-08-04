"""
MemDao модель DAO для работы с мемами в базе данных.
"""

from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import MappedColumn, mapped_column

from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.value_objects.image_path import ImagePath
from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID
from app.core.shared_kernel.db.dao import BaseDao


class MemDao(BaseDao):
    """
    Модель DAO для работы с мемами в базе данных.

    :cvar __tablename__: Название таблицы в базе данных.
    :cvar id: Уникальный идентификатор мема, первичный ключ.
    :cvar text: Текст мема.
    :cvar image_path: Путь к картинке мема.
    """

    __tablename__ = "memes"

    id: MappedColumn[UUID] = mapped_column(primary_key=True)
    text: MappedColumn[str] = mapped_column(String)
    image_path: MappedColumn[str | None] = mapped_column(String, nullable=True)

    def to_entity(self) -> Mem:
        """
        Создаёт сущность мема из модели DAO.

        :return: Созданная сущность мема.
        """
        image_path = ImagePath(self.image_path) if self.image_path else None

        return Mem(
            uuid=MemUUID(self.id),
            text=MemText(self.text),
            image_path=image_path
        )

    @classmethod
    def from_entity(cls, entity: Mem) -> "MemDao":
        """
        Создаёт модель DAO из сущности мема.

        :param entity: Сущность мема.
        :return: Созданная модель DAO мема.
        """
        image_path = entity.image_path.path if entity.image_path else None

        return cls(
            id=entity.uuid.uuid,
            text=entity.text.text,
            image_path=image_path
        )
