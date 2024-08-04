"""
Объект значение пути к картинке мема.
"""

from dataclasses import dataclass

from app.core.mem.domain.exceptions.base_mem_exceptions import MemTypeError


@dataclass(slots=True)
class ImagePath:
    """
    Объект значение пути к картинке мема.

    :ivar path: Путь к картинке мема.
    """

    path: str

    def __post_init__(self):
        """
        Проверяет путь на тип данных
        """
        if not isinstance(self.path, str):
            raise MemTypeError(extra_msg_exception='Путь к картинке мема должен быть типа `str`')
