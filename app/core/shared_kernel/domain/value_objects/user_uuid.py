"""
Объект значение уникального идентификатора пользователя.
"""

from dataclasses import dataclass
from uuid import UUID

from app.core.user.domain.exceptions.base_user_exceptions import UserTypeError


@dataclass(slots=True)
class UserUUID:
    """
    Объект значение уникального идентификатора пользователя.

    :ivar uuid: Уникальный идентификатор пользователя.
    """

    uuid: UUID

    def __post_init__(self):
        """
        Проверяет идентификатор на тип данных
        """
        if not isinstance(self.uuid, UUID):
            raise UserTypeError(extra_msg_exception='Идентификатор пользователя должен быть типом `UUID`')
