"""
Схема пользователя из токена.
"""
from uuid import UUID

from pydantic import BaseModel

from app.core.shared_kernel.domain.value_objects.user_role import UserRole


class UserFromTokenSchema(BaseModel):
    """
    Схема пользователя из токена.

    :cvar uuid: Идентификатор пользователя.
    :cvar role: Роль пользователя.
    :cvar token_id: Идентификатор токена.
    """

    uuid: UUID
    role: UserRole
    token_id: str
