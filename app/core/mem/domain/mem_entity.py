"""
Сущность мема.
"""

from dataclasses import dataclass

from app.core.mem.domain.value_objects.image_path import ImagePath
from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID
from app.core.shared_kernel.domain.entity import BaseEntity


@dataclass(slots=True, eq=False)
class Mem(BaseEntity):
    """
    Представляет сущность мема и его бизнес-логику.

    :cvar uuid: Уникальный идентификатор мема.
    :cvar text: Текст мема.
    :cvar image_path: Путь к изображению мема в S3 хранилище.
    """

    uuid: MemUUID
    text: MemText
    image_path: ImagePath | None = None
