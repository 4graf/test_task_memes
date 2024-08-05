"""
Функции для получения зависимостей пользователей.
Включает в себя создание сервиса пользователей.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.shared_kernel.db.dependencies import get_async_db_session
from app.core.user.application.user.services.user_service import UserService
from app.core.user.infrastructure.repositories.user_repository import UserDBRepository


async def get_user_service(session: AsyncSession = Depends(get_async_db_session)) -> UserService:
    """
    Получает сервис пользователей.

    :param session: Асинхронная сессия базы данных.
    :return: Сервис пользователей.
    """
    user_repository = UserDBRepository(session)
    return UserService(user_repository)
