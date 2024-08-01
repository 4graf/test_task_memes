"""
Объект значение текста мемов.
"""

from dataclasses import dataclass

from app.core.mem.domain.exceptions.mem_text_exceptions import MinLengthMemTextError, MaxLengthMemTextError


@dataclass(slots=True)
class MemText:
    """
    Объект значение текста мемов с валидацией

    :ivar text: Текст мема.
    """

    text: str

    def __post_init__(self):
        """
        Проверяет текст на длину
        """
        if len(self.text) < 5:
            raise MinLengthMemTextError
        if len(self.text) > 500:
            raise MaxLengthMemTextError
