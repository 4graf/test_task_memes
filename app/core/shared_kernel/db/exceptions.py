"""
Исключения при работе с базой данных.
"""


class EntityExistsException(Exception):
    """
    Исключение, возникающее при попытке добавить уже существующую сущность.
    """
    def __init__(self, msg='Сущность уже существует.'):
        """
        Конструктор EntityExistsException.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)


class EntityNotFoundException(Exception):
    """
    Исключение, возникающее при ненахождении сущности.
    """
    def __init__(self, msg='Сущность не найдена.'):
        """
        Конструктор EntityNotFoundException.

        :param msg: Сообщение исключения.
        """
        super().__init__(msg)

