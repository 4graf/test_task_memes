"""
Интерфейс репозитория для сущности пользователя UserRepository.
"""
from abc import ABC, abstractmethod
from typing import Sequence

from app.core.shared_kernel.domain.repository import BaseRepository
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
