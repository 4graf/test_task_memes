"""
Реализация репозитория базы данных для мемов MemDBRepository.
"""

from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.mem_repository import MemRepository
from app.core.mem.infrastructure.models.mem_dao import MemDao
from app.core.shared_kernel.db.repository import BaseDBRepository


class MemDBRepository(MemRepository, BaseDBRepository[Mem]):
    """
    Реализация репозитория базы данных для мемов.

    :cvar dao: DAO модель для работы с мемами в базе данных.
    """
    @property
    def dao(self) -> type[MemDao]:
        return MemDao
