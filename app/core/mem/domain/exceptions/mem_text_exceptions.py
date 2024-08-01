"""
Исключения для текста мема в доменном слое.
"""

from app.core.mem.domain.exceptions.base_mem_exceptions import MemValidationException


class MinLengthMemTextError(MemValidationException):
    """
    Исключение, возникающее при длине текста мема меньшей минимальной.
    """
    def __init__(self, msg: str = 'Длина текста мема меньше минимальной', min_length: int = None):
        """
        Конструктор MinLengthMemTextError.

        :param msg: Сообщение исключения.
        :param min_length: Минимальная длина для текста мема.
        """
        if min_length:
            msg = f'{msg} [{min_length}]'
        super().__init__(msg)


class MaxLengthMemTextError(MemValidationException):
    """
    Исключение, возникающее при длине текста мема большей максимальной.
    """
    def __init__(self, msg='Длина текста мема больше максимальной', max_length=None):
        """
        Конструктор MaxLengthMemTextError.

        :param msg: Сообщение исключения.
        :param max_length: Максимальная длина для текста мема.
        """
        if max_length:
            msg = f'{msg} [{max_length}]'
        super().__init__(msg)
