"""
Объект значение хэша пароля.
"""
from dataclasses import dataclass

from app.core.user.domain.exceptions.base_user_exceptions import UserTypeError


@dataclass(slots=True)
class PasswordHash:
    """
    Объект значение хэша пароля.

    :ivar password_hash: Хэш пароля.
    """

    password_hash: str

    def __post_init__(self):
        """
        Проверяет хэш пароля на тип данных
        """
        if not isinstance(self.password_hash, str):
            raise UserTypeError(extra_msg_exception='Хэш пароля должен быть типа `str`')
