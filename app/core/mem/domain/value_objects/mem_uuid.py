"""
Объект значение уникального идентификатора мемов.
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class MemUUID:
    """
    Объект значение уникального идентификатора мемов.

    :ivar uuid: Уникальный идентификатор мема.
    """

    uuid: UUID
