from abc import ABC

from app.core.mem.domain.mem_entity import Mem
from app.core.shared_kernel.domain.repository import BaseRepository


class AnecdoteRepository(BaseRepository[Mem], ABC):
    """
    Интерфейс репозитория для сущности Mem
    """
