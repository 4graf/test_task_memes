"""
MemDao модель DAO для работы с мемами в базе данных.
"""

from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import MappedColumn, mapped_column

from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID
from app.core.shared_kernel.db.dao import BaseDao


class MemDao(BaseDao):
    """
    Модель DAO для работы с мемами в базе данных.

    :cvar __table__: Название таблицы для объекта :class:`sqlalchemy.schema.Table`.
    :cvar id: Уникальный идентификатор мема, первичный ключ.
    :cvar text: Текст мема
    """

    __table__ = "memes"

    id: MappedColumn[UUID] = mapped_column(primary_key=True)
    text: MappedColumn[str] = mapped_column(String)

    def to_entity(self) -> Mem:
        """
        Создаёт сущность мема из модели DAO.

        :return: Созданная сущность мема.
        """

        return Mem(
            uuid=MemUUID(self.id),
            text=MemText(self.text)
        )

    @classmethod
    def from_entity(cls, entity: Mem) -> "MemDao":
        """
        Создаёт модель DAO из сущности мема.

        :param entity: Сущность мема.
        :return: Созданная модель DAO мема.
        """

        return cls(
            id=entity.uuid.uuid,
            text=entity.text.text
        )
