"""
Интерфейс репозитория для сущности мемов MemRepository.
"""

from abc import ABC

from app.core.mem.domain.mem_entity import Mem
from app.core.shared_kernel.domain.repository import BaseRepository


class MemRepository(BaseRepository[Mem], ABC):
    """
    Интерфейс репозитория для сущности мемов.
    """
