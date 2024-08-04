"""
UserDao модель DAO для работы с пользователями в базе данных.
"""
import enum
from uuid import UUID

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.shared_kernel.db.dao import BaseDao
from app.core.user.domain.user_entity import User
from app.core.user.domain.value_object.email import Email
from app.core.user.domain.value_object.login import Login
from app.core.user.domain.value_object.password_hash import PasswordHash
from app.core.user.domain.value_object.user_name import UserName
from app.core.shared_kernel.domain.value_objects.user_role import UserRole
from app.core.shared_kernel.domain.value_objects.user_uuid import UserUUID


class UserDao(BaseDao):
    """
    Модель DAO для работы с пользователями в базе данных.

    :cvar __tablename__: Название таблицы в базе данных.
    :cvar id: Уникальный идентификатор пользователя, первичный ключ.
    :cvar login: Логин пользователя.
    :cvar password_hash: Хэш пароля пользователя.
    :cvar email: Почтовый адрес пользователя.
    :cvar first_name: Имя пользователя.
    :cvar second_name: Фамилия пользователя.
    :cvar role: Роль пользователя.
    """

    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    first_name: Mapped[str] = mapped_column(String)
    second_name: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[enum.Enum] = mapped_column(Enum(UserRole))

    def to_entity(self) -> User:
        """
        Создаёт сущность пользователя из модели DAO.

        :return: Созданная сущность пользователя.
        """
        return User(
            uuid=UserUUID(self.id),
            login=Login(self.login),
            password_hash=PasswordHash(self.password_hash),
            email=Email(self.email),
            name=UserName(first_name=self.first_name,
                          second_name=self.second_name),
            role=UserRole(self.role)
        )

    @classmethod
    def from_entity(cls, entity: User) -> "UserDao":
        """
        Создаёт модель DAO из сущности пользователя.

        :param entity: Сущность пользователя.
        :return: Созданная модель DAO пользователя.
        """
        return cls(
            id=entity.uuid.uuid,
            login=entity.login.login,
            password_hash=entity.password_hash.password_hash,
            email=entity.email.email,
            first_name=entity.name.first_name,
            second_name=entity.name.second_name,
            role=entity.role
        )
