"""
Функции для получения зависимостей мемов.
Включает в себя создание сервиса мемов.
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.mem.application.services.mem_service import MemService
from app.core.mem.infrastructure.repositories.mem_repository import MemDBRepository
from app.core.shared_kernel.db.dependencies import get_async_db_session


async def get_mem_service(session: AsyncSession = Depends(get_async_db_session)) -> MemService:
    """
    Получает сервис мемов.

    :param session: Асинхронная сессия базы данных.
    :return: Сервис мемов.
    """

    mem_repository = MemDBRepository(session)
    return MemService(mem_repository)
