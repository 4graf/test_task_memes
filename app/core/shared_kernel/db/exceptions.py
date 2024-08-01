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
