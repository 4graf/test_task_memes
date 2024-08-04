"""
Схема данных пользователя для токена.
"""
from pydantic import BaseModel


class UserToTokenSchema(BaseModel):
    """
    Схема данных пользователя для токена.

    :cvar uuid: Идентификатор пользователя.
    :cvar role: Роль пользователя.
    """

    uuid: str
    role: str
