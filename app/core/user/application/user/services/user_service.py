"""
Сервис для работы с пользователями UserService.
"""
from uuid import UUID

from app.core.shared_kernel.db.exceptions import EntityNotFoundException, EntityExistsException
from app.core.shared_kernel.domain.value_objects.user_uuid import UserUUID
from app.core.user.application.user.exceptions import UserNotFoundException, UserExistsException
from app.core.user.application.user.schemas.user_read_schema import UserReadSchema
from app.core.user.application.user.schemas.user_update_schema import UserUpdateSchema
from app.core.user.domain.user_entity import User
from app.core.user.domain.user_repository import UserRepository
from app.core.user.domain.value_object.email import Email
from app.core.user.domain.value_object.login import Login
from app.core.user.domain.value_object.password_hash import PasswordHash
from app.core.user.domain.value_object.user_name import UserName


class UserService:
    """
    Сервис для работы с пользователями UserService.

    :ivar user_repository: Репозиторий пользователей.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Конструктор UserService.

        :param user_repository: Репозиторий пользователей.
        """
        self.user_repository = user_repository

    async def get_user_by_id(self, id_: UUID) -> UserReadSchema:
        """
        Получает информацию о пользователе по его идентификатору.

        :param id_: Уникальный идентификатор пользователя.
        :return: Информация о пользователе.
        :raise UserNotFoundException: Пользователь не был найден.
        """
        user = await self.user_repository.get_by_id(id_)
        if not user:
            raise UserNotFoundException

        return UserReadSchema.from_entity(user)

    async def get_user_by_login(self, user_login: str) -> UserReadSchema:
        """
        Получает информацию о пользователе по его логину.

        :param user_login: Логин пользователя.
        :return: Информация о пользователе.
        :raise UserNotFoundException: Пользователь не был найден.
        """
        user = await self.user_repository.get_by_login(user_login)
        if not user:
            raise UserNotFoundException

        return UserReadSchema.from_entity(user)

    async def get_all_user(self) -> list[UserReadSchema]:
        """
        Получает информацию о всех пользователях.

        :return: Список с информациями о пользователях.
        """
        users = await self.user_repository.get_all()

        return [UserReadSchema.from_entity(user) for user in users]

    async def update_user(self, data: UserUpdateSchema) -> UserReadSchema:
        """
        Обновляет пользователя.

        :param data: Данные для обновления пользователя.
        :return: Информация обновленного пользователя.
        :raise UserNotFoundException: Обновление пользователя, который не найден.
        :raise UserExistsException: Добавление пользователя, который уже существует.
        """
        try:
            old_user = await self.user_repository.get_by_id(data.uuid)

            user = User(
                uuid=UserUUID(data.uuid),
                login=Login(data.login),
                password_hash=PasswordHash(data.password),
                email=Email(data.email),
                name=UserName(first_name=data.name.first_name,
                              second_name=data.name.second_name),
                role=old_user.role
            )
            await self.user_repository.update(user)
        except EntityNotFoundException as e:
            raise UserNotFoundException from e
        except EntityExistsException as e:
            raise UserExistsException from e

        return UserReadSchema.from_entity(user)