"""
Объект значение пути к картинке мема.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ImagePath:
    """
    Объект значение пути к картинке мема.

    :ivar path: Путь к картинке мема.
    """

    path: str
