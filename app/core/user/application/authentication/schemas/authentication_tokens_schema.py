"""
Пара токенов доступа и обновления.
"""
from pydantic import BaseModel

from app.core.user.application.authentication.schemas.access_token_schema import AccessTokenSchema
from app.core.user.application.authentication.schemas.refresh_token_schema import RefreshTokenSchema


class AuthenticationTokensSchema(BaseModel):
    """
    Пара токенов доступа и обновления.

    :cvar access_token: Токен доступа
    :cvar refresh_token: Токен обновления
    """
    access_token: AccessTokenSchema
    refresh_token: RefreshTokenSchema
