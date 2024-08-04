"""
Базовое исключение для аутентификации.
"""


class AuthenticationException(Exception):
    """
    Базовое исключение для аутентификации.
    """


class WrongPasswordException(AuthenticationException):
    """
    Исключение, возникающее если ввод учётных данных неверен.
    """
    def __init__(self, msg='Учётные данные введены неверно.'):
        """
        Конструктор WrongPasswordException.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)


class TokenExpiredException(AuthenticationException):
    """
    Исключение, возникающее если время жизни токена истекло.
    """
    def __init__(self, msg='Время жизни токена истекло.'):
        """
        Конструктор TokenExpiredException.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)


class TokenCorruptedException(AuthenticationException):
    """
    Исключение, возникающее если токен повреждён.
    """
    def __init__(self, msg='Токен повреждён.'):
        """
        Конструктор TokenCorruptedException.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)

