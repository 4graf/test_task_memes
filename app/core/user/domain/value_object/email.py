"""
Объект значение почтового адреса.
"""
import re
from dataclasses import dataclass

from app.core.user.domain.exceptions.email_exceptions import MaxLengthEmailError, IncorrectEmailError


def validate_email(email: str) -> bool:
    email_regex = r'[^@]+@[^@]+\.[^@]+'
    if re.fullmatch(email_regex, email):
        return True
    return False


@dataclass(slots=True)
class Email:

    """
    Объект значение почтового адреса.

    :ivar email: Почтовый адрес.
    """
    email: str

    def __post_init__(self):
        """
        Проверяет почтовый адрес на корректность и длину.
        """
        if len(self.email) > 70:
            raise MaxLengthEmailError(max_length=70)
        
        if not validate_email(self.email):
            raise IncorrectEmailError
        