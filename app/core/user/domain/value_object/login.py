"""
Объект значение логина.
"""

from dataclasses import dataclass

from app.core.user.domain.exceptions.base_user_exceptions import UserTypeError
from app.core.user.domain.exceptions.login_exceptions import MinLengthLoginError, MaxLengthLoginError


@dataclass(slots=True)
class Login:
    """
    Объект значение логина

    :ivar login: Логин.
    """

    login: str

    def __post_init__(self):
        """
        Проверяет логин на тип данных и длину
        """
        if not isinstance(self.login, str):
            raise UserTypeError(extra_msg_exception='Текст мема должен быть типом `str`')
        if len(self.login) < 8:
            raise MinLengthLoginError(min_length=8)
        if len(self.login) > 50:
            raise MaxLengthLoginError(max_length=50)
