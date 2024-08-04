"""
Токен обновления и его тип.
"""
from pydantic import BaseModel


class RefreshTokenSchema(BaseModel):
    """
    Токен обновления и его тип.

    :cvar refresh_token: Токен
    :cvar token_type: Тип токена
    """
    refresh_token: str
    token_type: str
