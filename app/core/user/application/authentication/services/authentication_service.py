"""
Сервис аутентификации.
"""
from uuid import uuid4

from app.core.shared_kernel.db.exceptions import EntityExistsException
from app.core.shared_kernel.domain.value_objects.user_role import UserRole
from app.core.shared_kernel.domain.value_objects.user_uuid import UserUUID
from app.core.user.application.authentication.exceptions import WrongPasswordException
from app.core.user.application.authentication.schemas.authentication_tokens_schema import AuthenticationTokensSchema
from app.core.user.application.authentication.schemas.user_login_schema import UserLoginSchema
from app.core.user.application.authentication.schemas.user_register_schema import UserRegisterSchema
from app.core.user.application.authentication.schemas.user_to_token_schema import UserToTokenSchema
from app.core.user.application.authentication.services.password_service import PasswordService
from app.core.user.application.authentication.services.token_service import TokenService
from app.core.user.application.user.exceptions import UserExistsException, UserNotFoundException
from app.core.user.domain.user_entity import User
from app.core.user.domain.user_repository import UserRepository
from app.core.user.domain.value_object.email import Email
from app.core.user.domain.value_object.login import Login
from app.core.user.domain.value_object.password_hash import PasswordHash
from app.core.user.domain.value_object.user_name import UserName
from app.settings import AuthenticationSettings

settings = AuthenticationSettings()


class AuthenticationService:
    """
    Сервис аутентификации.

    :ivar user_repository: Репозиторий пользователей.
    """
    def __init__(self, user_repository: UserRepository):
        """
        Конструктор AuthenticationService.

        :param user_repository: Репозиторий пользователей.
        """
        self.user_repository = user_repository

    async def register_user(self, data: UserRegisterSchema) -> AuthenticationTokensSchema:
        """
        Регистрирует нового пользователя.

        :param data: Данные пользователя.
        :return: Пара токенов доступа и обновления.
        """
        user = User(
            uuid=UserUUID(uuid4()),
            login=Login(data.login),
            password_hash=PasswordHash(PasswordService.hash_password(data.password)),
            email=Email(data.email),
            name=UserName(first_name=data.name.first_name,
                          second_name=data.name.second_name),
            role=UserRole.USER
        )
        try:
            await self.user_repository.add(user)
        except EntityExistsException as e:
            raise UserExistsException from e

        user_to_token = UserToTokenSchema(uuid=str(user.uuid.uuid),
                                          role=user.role.name)
        access_token = TokenService.create_access_token(user_to_token)
        refresh_token = TokenService.create_refresh_token(user_to_token)
        return AuthenticationTokensSchema(access_token=access_token,
                                          refresh_token=refresh_token)

    async def login(self, user_login: UserLoginSchema) -> AuthenticationTokensSchema:
        """
        Авторизовывает пользователя.

        :param user_login: Данные пользователя.
        :return: Пара токенов доступа и обновления.
        """
        user = await self.user_repository.get_by_login(user_login.login)
        if not user:
            raise UserNotFoundException
        if not PasswordService.validate_password(user_login.password, user.password_hash.password_hash):
            raise WrongPasswordException

        user_to_token = UserToTokenSchema(uuid=str(user.uuid.uuid),
                                          role=user.role.value)
        access_token = TokenService.create_access_token(user_to_token)
        refresh_token = TokenService.create_refresh_token(user_to_token)
        return AuthenticationTokensSchema(access_token=access_token,
                                          refresh_token=refresh_token)

    async def logout(self):
        #  Добавить Redis и вести учёт деактивированных токенов
        ...

    async def refresh(self, refresh_token: str) -> AuthenticationTokensSchema:
        user_data = TokenService.decode_refresh_token(refresh_token)

        ...  # Удаление всего семейства старых токенов в Redis

        if not await self.user_repository.get_by_id(user_data.uuid):
            raise UserNotFoundException

        user_to_token = UserToTokenSchema(uuid=str(user_data.uuid),
                                          role=user_data.role)
        new_access_token = TokenService.create_access_token(user_to_token)
        new_refresh_token = TokenService.create_refresh_token(user_to_token)

        return AuthenticationTokensSchema(access_token=new_access_token,
                                          refresh_token=new_refresh_token)
