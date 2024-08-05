"""
Интерфейс репозитория для сущности мемов MemRepository.
"""

from abc import ABC, abstractmethod
from typing import Sequence

from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.utils.mem_filter_params import MemFilterParams
from app.core.shared_kernel.domain.repository import BaseRepository


class MemRepository(BaseRepository[Mem], ABC):
    """
    Интерфейс репозитория для сущности мемов.
    """

    @abstractmethod
    async def get_by_filter(self, mem_filter_params: MemFilterParams) -> Sequence[Mem]:
        """
        Получает сущность мема по фильтру.

        :param mem_filter_params: Параметры фильтра.
        :return: Список отфильтрованных мемов.
        """
        ...
