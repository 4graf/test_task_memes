"""
Исключения для имени пользователя в доменном слое.
"""

from app.core.user.domain.exceptions.base_user_exceptions import UserValidationException


class MinLengthUserFirstNameError(UserValidationException):
    """
    Исключение, возникающее при длине имени меньшей минимальной.
    """
    def __init__(self, msg: str = 'Длина имени меньше минимальной', min_length: int = None):
        """
        Конструктор MinLengthUserFirstNameError.

        :param msg: Сообщение исключения.
        :param min_length: Минимальная длина для имени.
        """
        if min_length:
            msg = f'{msg} [{min_length}]'
        super().__init__(msg)


class MaxLengthUserFirstNameError(UserValidationException):
    """
    Исключение, возникающее при длине имени большей максимальной.
    """
    def __init__(self, msg: str = 'Длина имени больше максимальной', max_length: int = None):
        """
        Конструктор MaxLengthUserFirstNameError.

        :param msg: Сообщение исключения.
        :param max_length: Максимальная длина имени.
        """
        if max_length:
            msg = f'{msg} [{max_length}]'
        super().__init__(msg)


class MinLengthUserSecondNameError(UserValidationException):
    """
    Исключение, возникающее при длине фамилии меньшей минимальной.
    """
    def __init__(self, msg: str = 'Длина фамилии меньше минимальной', min_length: int = None):
        """
        Конструктор MinLengthUserSecondNameError.

        :param msg: Сообщение исключения.
        :param min_length: Минимальная длина для фамилии.
        """
        if min_length:
            msg = f'{msg} [{min_length}]'
        super().__init__(msg)


class MaxLengthUserSecondNameError(UserValidationException):
    """
    Исключение, возникающее при длине фамилии большей максимальной.
    """
    def __init__(self, msg: str = 'Длина фамилии больше максимальной', max_length: int = None):
        """
        Конструктор MaxLengthUserSecondNameError.

        :param msg: Сообщение исключения.
        :param max_length: Максимальная длина фамилии.
        """
        if max_length:
            msg = f'{msg} [{max_length}]'
        super().__init__(msg)
