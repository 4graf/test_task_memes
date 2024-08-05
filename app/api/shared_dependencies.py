"""
Общие зависимости для апи.
"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.shared_kernel.db.dependencies import get_async_db_session
from app.core.user.application.authentication.schemas.user_from_token_schema import UserFromTokenSchema
from app.core.user.application.authentication.services.token_service import TokenService
from app.core.user.application.user.schemas.user_read_schema import UserReadSchema
from app.core.user.application.user.services.user_service import UserService
from app.core.user.infrastructure.repositories.user_repository import UserDBRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user_role(access_token: Annotated[str, Depends(oauth2_scheme)]) -> UserFromTokenSchema:
    """
    Декодирует токен доступа и возвращает данные.
    :param access_token: Токен доступа.
    :return: Данные пользователя из токена
    """
    return TokenService.decode_access_token(access_token)


async def get_current_user_info(access_token: Annotated[str, Depends(oauth2_scheme)],
                                session: AsyncSession = Depends(get_async_db_session)) -> UserReadSchema:
    """
    Декодирует токен доступа и получает данные пользователя из репозитория.
    :param access_token: Токен доступа.
    :param session: Асинхронная сессия БД.
    :return: Данные пользователя.
    """
    user_repository = UserDBRepository(session)
    user_service = UserService(user_repository)

    token_data = TokenService.decode_access_token(access_token)

    user = await user_service.get_user_by_id(token_data.uuid)
    return user
