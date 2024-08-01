"""
Сущность мема.
"""

from dataclasses import dataclass

from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID
from app.core.shared_kernel.domain.entity import BaseEntity


@dataclass(slots=True)
class Mem(BaseEntity):
    """
    Представляет сущность мема и его бизнес-логику.

    :cvar uuid: Уникальный идентификатор мема.
    :cvar text: Текст мема.
    """
    uuid: MemUUID
    text: MemText
