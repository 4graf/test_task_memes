"""
Объект значение имя пользователя.
"""
from dataclasses import dataclass

from app.core.user.domain.exceptions.base_user_exceptions import UserTypeError, UserException
from app.core.user.domain.exceptions.user_name_exceptions import MinLengthUserFirstNameError, \
    MaxLengthUserFirstNameError, MinLengthUserSecondNameError, MaxLengthUserSecondNameError


def validate_name(name: str, less_exception: type[UserException], greater_exception: type[UserException]) -> None:
    if len(name) < 2:
        raise less_exception
    if len(name) > 60:
        raise greater_exception


@dataclass(slots=True)
class UserName:
    """
    Объект значение имя пользователя.

    :ivar first_name: Имя пользователя.
    :ivar second_name: Фамилия пользователя.
    """
    first_name: str
    second_name: str | None

    def __post_init__(self):
        """
        Проверяет имя и фамилию пользователя на корректность.
        """
        if not isinstance(self.first_name, str):
            raise UserTypeError(extra_msg_exception='Имя пользователя должно быть типа `str`')
        validate_name(self.first_name, MinLengthUserFirstNameError, MaxLengthUserFirstNameError)

        if self.second_name is not None:
            if not isinstance(self.first_name, str):
                raise UserTypeError(extra_msg_exception='Фамилия пользователя должно быть типа `str`')
            validate_name(self.second_name, MinLengthUserSecondNameError, MaxLengthUserSecondNameError)
