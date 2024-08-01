"""
Исключения для мемов в слое приложения.
"""
from app.core.mem.domain.exceptions.base_mem_exceptions import MemException


class MemNotFoundException(MemException):
    """
    Исключение, возникающее если мем не был найден.
    """

    def __init__(self, msg: str = 'Мем не был найден'):
        """
        Конструктор MemNotFoundException.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)


class MemExistsException(MemException):
    """
    Исключение, возникающее если добавленный мем уже существует.
    """

    def __init__(self, msg: str = 'Мем уже существует'):
        """
        Конструктор MemExistsException.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)
