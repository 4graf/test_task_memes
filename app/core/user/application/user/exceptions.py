"""
Исключения для пользователей в слое приложения.
"""
from app.core.user.domain.exceptions.base_user_exceptions import UserException


class UserNotFoundException(UserException):
    """
    Исключение, возникающее если пользователь не был найден.
    """

    def __init__(self, msg: str = 'Пользователь не был найден'):
        """
        Конструктор UserNotFoundException.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)


class UserExistsException(UserException):
    """
    Исключение, возникающее если добавленный пользователь уже существует.
    """

    def __init__(self, msg: str = 'Пользователь уже существует'):
        """
        Конструктор UserExistsException.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)
