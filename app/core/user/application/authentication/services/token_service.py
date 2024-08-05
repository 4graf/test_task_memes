"""
Сервис для работы с JWT токенами.
"""
from datetime import datetime, timedelta
from uuid import uuid4, UUID

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.shared_kernel.domain.value_objects.user_role import UserRole
from app.core.user.application.authentication.exceptions import TokenExpiredException, TokenCorruptedException
from app.core.user.application.authentication.schemas.access_token_schema import AccessTokenSchema
from app.core.user.application.authentication.schemas.refresh_token_schema import RefreshTokenSchema
from app.core.user.application.authentication.schemas.user_from_token_schema import UserFromTokenSchema
from app.core.user.application.authentication.schemas.user_to_token_schema import UserToTokenSchema
from app.settings import AuthenticationSettings

settings = AuthenticationSettings()


class TokenService:
    """
    Сервис для работы с JWT токенами.
    """

    @classmethod
    def create_access_token(cls, data: UserToTokenSchema) -> AccessTokenSchema:
        """
        Создаёт токен доступа.
        :param data: Информация о пользователе.
        :return: Токен доступа
        """
        to_encode = data.model_dump()
        encoded_jwt = cls._create(data=to_encode,
                                  expiration=settings.access_expiration,
                                  secret_key=settings.access_secret_key)
        return AccessTokenSchema(access_token=encoded_jwt,
                                 token_type="Bearer")

    @classmethod
    def decode_access_token(cls, access_token: str) -> UserFromTokenSchema:
        """
        Декодирует токен доступа.
        :param access_token: Токен доступа.
        :return: Информация о пользователе.
        """
        data = cls._decode(token=access_token, secret_key=settings.access_secret_key)
        user = UserFromTokenSchema(uuid=UUID(data['uuid']),
                                   role=UserRole(data['role']),
                                   token_id=data['token_id'])
        return user

    @classmethod
    def create_refresh_token(cls, data: UserToTokenSchema) -> RefreshTokenSchema:
        """
        Создаёт токен обновления.
        :param data: Информация о пользователе.
        :return: Токен обновления
        """
        to_encode = data.model_dump()
        encoded_jwt = cls._create(data=to_encode,
                                  expiration=settings.refresh_expiration,
                                  secret_key=settings.refresh_secret_key)
        return RefreshTokenSchema(refresh_token=encoded_jwt,
                                  token_type="Bearer")

    @classmethod
    def decode_refresh_token(cls, refresh_token: str) -> UserFromTokenSchema:
        """
        Декодирует токен обновления.
        :param refresh_token: Токен обновления.
        :return: Информация о пользователе.
        """
        data = cls._decode(token=refresh_token, secret_key=settings.refresh_secret_key)
        user = UserFromTokenSchema(uuid=UUID(data['uuid']),
                                   role=UserRole(data['role']),
                                   token_id=data['token_id'])
        return user

    @classmethod
    def _create(cls, data: dict, expiration: int, secret_key: str) -> str:
        """
        Кодирует информацию в токен.
        :param data: Информация.
        :param expiration: Время жизни токена.
        :param secret_key: Секретный ключ.
        :return: Токен
        """
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=expiration)
        to_encode['exp'] = expire
        token_id = str(uuid4())
        to_encode['token_id'] = token_id
        encoded_jwt = jwt.encode(to_encode, secret_key, settings.jwt_algorithm)
        return encoded_jwt

    @classmethod
    def _decode(cls, token: str, secret_key: str) -> dict:
        """
        Декодирует токен.
        :param token: Токен.
        :param secret_key: Секретный ключ.
        :return: Словарь с информацией.
        """
        try:
            data = jwt.decode(token, secret_key, [settings.jwt_algorithm])
        except ExpiredSignatureError as e:
            raise TokenExpiredException from e
        except InvalidTokenError as e:
            raise TokenCorruptedException from e

        return data
