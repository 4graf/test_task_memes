"""
Исключения для логина в доменном слое.
"""

from app.core.user.domain.exceptions.base_user_exceptions import UserValidationException


class MinLengthLoginError(UserValidationException):
    """
    Исключение, возникающее при длине логина меньшей минимальной.
    """
    def __init__(self, msg: str = 'Длина логина меньше минимальной', min_length: int = None):
        """
        Конструктор MinLengthLoginError.

        :param msg: Сообщение исключения.
        :param min_length: Минимальная длина для логина.
        """
        if min_length:
            msg = f'{msg} [{min_length}]'
        super().__init__(msg)


class MaxLengthLoginError(UserValidationException):
    """
    Исключение, возникающее при длине логина большей максимальной.
    """
    def __init__(self, msg: str = 'Длина логина больше максимальной', max_length: int = None):
        """
        Конструктор MaxLengthLoginError.

        :param msg: Сообщение исключения.
        :param max_length: Максимальная длина логина.
        """
        if max_length:
            msg = f'{msg} [{max_length}]'
        super().__init__(msg)
