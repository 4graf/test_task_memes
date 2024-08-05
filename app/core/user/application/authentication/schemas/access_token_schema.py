"""
Токен доступа и его тип.
"""
from pydantic import BaseModel


class AccessTokenSchema(BaseModel):
    """
    Токен доступа и его тип.

    :cvar access_token: Токен
    :cvar token_type: Тип токена
    """
    access_token: str
    token_type: str
