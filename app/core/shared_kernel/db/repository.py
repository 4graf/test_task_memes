"""
Базовый репозиторий базы данных для работы с DAO моделью BaseDBRepository.
"""

from abc import ABC, abstractmethod
from typing import Sequence, TypeVar
from uuid import UUID

from sqlalchemy import insert, update, select, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.shared_kernel.db.dao import BaseDao
from app.core.shared_kernel.db.exceptions import EntityExistsException
from app.core.shared_kernel.domain.entity import BaseEntity
from app.core.shared_kernel.domain.repository import BaseRepository

Entity = TypeVar("Entity", bound=BaseEntity)


class BaseDBRepository(BaseRepository[Entity], ABC):
    """
    Базовый репозиторий базы данных для работы с DAO моделью.

    :cvar dao: DAO модель для работы с мемами в базе данных.

    :ivar session: Асинхронная сессия базы данных.
    """

    @property
    @abstractmethod
    def dao(self) -> type[BaseDao]:
        ...
    
    def __init__(self, session: AsyncSession):
        """
        Конструктор BaseDBRepository.

        :param session: Асинхронная сессия базы данных.
        """
        self.session = session

    async def add(self, entity: Entity | list[Entity]) -> Entity | Sequence[Entity]:
        """
        Добавляет сущность в базу данных.

        :param entity: Сущность доменной области или список сущностей для добавления.
        :return: Добавленная сущность или список добавленных сущностей.
        :raise EntityExistsException: Нарушение целостности базы данных при добавлении сущности,
            которая уже существует.
        """

        add_dao = self.dao.from_entity(entity)
        stmt = (
            insert(self.dao)
            .values(add_dao.to_dict())
            .returning(self.dao)
        )
        try:
            result = await self.session.execute(stmt)
            result = result.scalars().all()
            await self.session.commit()
        except IntegrityError as e:
            raise EntityExistsException from e
        return result[0].to_entity() if len(result) == 1 else [dao.to_entity() for dao in result]

    async def update(self, entity: Entity) -> Entity:
        """
        Обновляет сущность в базе данных.

        :param entity: Сущность доменной области для обновления.
        :return: Обновлённая сущность.
        :raise EntityExistsException: Нарушение целостности базы данных при обновлении сущности,
            новая сущность уже существует.
        """

        update_dao = self.dao.from_entity(entity)
        stmt = (
            update(self.dao)
            .values(update_dao.to_dict())
            .filter_by(id=update_dao.id)
            .returning(self.dao)
        )

        try:
            result = await self.session.execute(stmt)
            result = result.scalar_one()
            await self.session.commit()
        except IntegrityError as e:
            raise EntityExistsException from e
        return result.to_entity()

    async def get_by_id(self, id_: UUID) -> Entity | None:
        """
        Получает сущность по её идентификатору.

        :param id_: Уникальный идентификатор сущности.
        :return: Сущность или None, если сущность не была найдена.
        """

        stmt = (
            select(self.dao)
            .filter_by(id=id_)
        )

        result = await self.session.execute(stmt)
        result = result.scalar_one_or_none()
        return result.to_entity() if result else None

    async def get_all(self) -> Sequence[Entity]:
        """
        Получает все сущности.

        :return: Список сущностей.
        """

        stmt = (
            select(self.dao)
        )

        try:
            result = await self.session.execute(stmt)
            result = result.scalars().all()
        except NoResultFound:
            return []

        return [dao.to_entity() for dao in result]

    async def delete_by_id(self, id_: UUID) -> None:
        """
        Удаляет сущность по его идентификатору.

        :param id_: Уникальный идентификатор сущности.
        """

        stmt = (
            delete(self.dao)
            .filter_by(id=id_)
        )

        await self.session.execute(stmt)
        await self.session.commit()
