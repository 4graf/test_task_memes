"""
Интерфейс репозитория с CRUD методами BaseRepository.
"""

from abc import ABC, abstractmethod
from typing import Sequence, Generic, TypeVar
from uuid import UUID

from app.core.shared_kernel.domain.entity import BaseEntity

Entity = TypeVar("Entity", bound=BaseEntity)


class BaseRepository(ABC, Generic[Entity]):
    """
        Интерфейс репозитория с CRUD методами.
    """

    @abstractmethod
    async def add(self, entity: Entity | list[Entity]) -> Entity | Sequence[Entity]:
        """
        Добавляет сущность в базу данных.

        :param entity: Сущность доменной области или список сущностей для добавления.
        :return: Добавленная сущность или список добавленных сущностей.
        """
        ...

    @abstractmethod
    async def update(self, entity: Entity) -> Entity:
        """
        Обновляет сущность в базе данных.

        :param entity: Сущность доменной области для обновления.
        :return: Обновлённая сущность.
        """
        ...

    @abstractmethod
    async def get_by_id(self, id_: UUID) -> Entity | None:
        """
        Получает сущность по её идентификатору.

        :param id_: Уникальный идентификатор сущности.
        :return: Сущность или None, если сущность не была найдена.
        """
        ...

    @abstractmethod
    async def get_all(self) -> Sequence[Entity]:
        """
        Получает все сущности.

        :return: Список сущностей.
        """
        ...

    @abstractmethod
    async def delete_by_id(self, id_: UUID) -> None:
        """
        Удаляет сущность по его идентификатору.

        :param id_: Уникальный идентификатор сущности.
        """
        ...

