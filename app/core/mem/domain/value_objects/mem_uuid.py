"""
Объект значение уникального идентификатора мемов.
"""

from dataclasses import dataclass
from uuid import UUID

from app.core.mem.domain.exceptions.mem_text_exceptions import MemTextTypeError


@dataclass(slots=True)
class MemUUID:
    """
    Объект значение уникального идентификатора мемов.

    :ivar uuid: Уникальный идентификатор мема.
    """

    uuid: UUID

    def __post_init__(self):
        """
        Проверяет идентификатор на тип данных
        """
        if not isinstance(self.uuid, UUID):
            raise MemTextTypeError(extra_msg_exception='Идентификатор мема должен быть типом `UUID`')
