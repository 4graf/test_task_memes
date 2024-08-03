"""
Базовые исключения для мемов.
"""


class MemException(Exception):
    """
    Базовое исключение для мемов.
    """


class MemValidationException(MemException):
    """
    Базовое исключение для валидации мемов.
    """


class MemTypeError(MemValidationException):
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
