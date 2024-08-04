"""
Реализация репозитория базы данных для мемов MemDBRepository.
"""
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.mem_repository import MemRepository
from app.core.mem.domain.utils.mem_filter_params import MemFilterParams
from app.core.mem.infrastructure.models.mem_dao import MemDao
from app.core.mem.infrastructure.repositories.utils.mem_filter import MemFilter
from app.core.shared_kernel.db.repository import BaseDBRepository


class MemDBRepository(MemRepository, BaseDBRepository[Mem]):
    """
    Реализация репозитория базы данных для мемов.

    :cvar dao: DAO модель для работы с мемами в базе данных.
    """
    @property
    def dao(self) -> type[MemDao]:
        return MemDao

    async def get_by_filter(self, mem_filter_params: MemFilterParams) -> list[Mem]:
        get_query = select(self.dao)
        filter_query = MemFilter.filter_query(query=get_query, mem_filter_params=mem_filter_params)
        try:
            result = await self.session.execute(filter_query)
            result = result.scalars().all()
        except NoResultFound:
            return []
        return [dao.to_entity() for dao in result]
