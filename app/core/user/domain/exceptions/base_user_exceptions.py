"""
Базовые исключения для пользователя.
"""


class UserException(Exception):
    """
    Базовое исключение для пользователя.
    """


class UserValidationException(UserException):
    """
    Базовое исключение для валидации пользователя.
    """


class UserTypeError(UserValidationException):
    """
    Исключение, возникающее при несоответствии типа данных.
    """
    def __init__(self, msg: str = 'Ошибка валидации', extra_msg_exception: str = None):
        """
        Конструктор MemTypeError.

        :param msg: Сообщение исключения.
        :param extra_msg_exception: Дополнительное сообщение исключения.
        """
        if extra_msg_exception:
            msg = f'{msg}: {extra_msg_exception}'
        super().__init__(msg)
