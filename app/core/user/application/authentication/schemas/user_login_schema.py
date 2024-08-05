"""
Схема учётных данных пользователя.
"""
from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    """
    Схема учётных данных пользователя.

    :cvar login: Логин пользователя.
    :cvar password: Пароль пользователя.
    """

    login: str
    password: str
