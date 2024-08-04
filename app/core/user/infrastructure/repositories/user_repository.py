"""
Реализация репозитория базы данных для пользователей UserDBRepository.
"""

from sqlalchemy import select

from app.core.shared_kernel.db.repository import BaseDBRepository
from app.core.user.domain.user_entity import User
from app.core.user.domain.user_repository import UserRepository
from app.core.user.infrastructure.models.user_dao import UserDao


class UserDBRepository(UserRepository, BaseDBRepository[User]):
    """
    Реализация репозитория базы данных для пользователей.

    :cvar dao: DAO модель для работы с пользователями в базе данных.
    """

    @property
    def dao(self) -> type[UserDao]:
        return UserDao

    async def get_by_login(self, login: str) -> User | None:
        """
        Получает сущность пользователя по логину.

        :param login: Логин пользователя.
        :return: Пользователь или None, если пользователь не был найден.
        """
        query = select(self.dao).filter_by(login=login)
        result = await self.session.execute(query)
        result = result.scalar_one_or_none()

        return result.to_entity() if result else None

