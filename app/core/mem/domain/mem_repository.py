from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from app.core.mem.domain.mem_entity import Mem
from app.core.shared_kernel.domain.repository import BaseRepository


class AnecdoteRepository(BaseRepository[Mem], ABC):
    """
        Объявляет интерфейс репозитория для сущности Anecdote
    """

    @abstractmethod
    async def get_user_anecdotes(self, user_id: UUID) -> Sequence[Anecdote]:
        ...
