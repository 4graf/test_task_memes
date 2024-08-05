"""
Исключения для почтового адреса в доменном слое.
"""

from app.core.user.domain.exceptions.base_user_exceptions import UserValidationException


class MaxLengthEmailError(UserValidationException):
    """
    Исключение, возникающее при длине почтового адреса большей максимальной.
    """
    def __init__(self, msg: str = 'Длина почтового адреса больше максимальной', max_length: int = None):
        """
        Конструктор MaxLengthEmailError.

        :param msg: Сообщение исключения.
        :param max_length: Максимальная длина почтового адреса.
        """
        if max_length:
            msg = f'{msg} [{max_length}]'
        super().__init__(msg)


class IncorrectEmailError(UserValidationException):
    """
    Исключение, возникающее при некорректной форме почтового адреса.
    """
    def __init__(self, msg: str = 'Почтовый адрес введён некорректно'):
        """
        Конструктор MaxLengthEmailError.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)
