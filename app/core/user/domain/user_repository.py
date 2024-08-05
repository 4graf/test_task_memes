"""
Интерфейс репозитория для сущности пользователя UserRepository.
"""
from abc import ABC, abstractmethod
from typing import Sequence

from app.core.shared_kernel.domain.repository import BaseRepository
from app.core.shared_kernel.domain.value_objects.user_role import UserRole
from app.core.user.domain.user_entity import User


class UserRepository(BaseRepository[User], ABC):
    """
    Интерфейс репозитория для сущности пользователя.
    """

    @abstractmethod
    async def get_by_login(self, login: str) -> User | None:
        """
        Получает сущность пользователя по логину.

        :param login: Логин пользователя.
        :return: Пользователь или None, если пользователь не был найден.
        """
        ...

    @abstractmethod
    async def get_by_role(self, role: UserRole) -> Sequence[User]:
        """
        Получает сущности пользователей по роли.

        :param role: Роль пользователя.
        :return: Список пользователей.
        """
        ...
