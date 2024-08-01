"""
BaseDao абстрактная базовая модель DAO.
"""

from abc import abstractmethod

from sqlalchemy.orm import DeclarativeBase

from app.core.shared_kernel.domain.entity import BaseEntity


class BaseDao(DeclarativeBase):
    """
    BaseDao абстрактная базовая модель DAO.

    :cvar __abstract__: Флаг для обозначения SQLAlchemy класса абстрактным
    """

    __abstract__ = True

    @abstractmethod
    def to_entity(self) -> BaseEntity:
        """
        Создаёт сущность из модели DAO.

        :return: Созданная сущность.
        """
        ...

    @classmethod
    @abstractmethod
    def from_entity(cls, entity: BaseEntity) -> "BaseDao":
        """
        Создаёт модель DAO из сущности.

        :param entity: Сущность.
        :return: Созданная модель DAO.
        """
        ...

    def to_dict(self):
        """
        Создаёт словарь из столбцов и их значений модели DAO.
        :return: Словарь вида {название столбца: значение}
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
