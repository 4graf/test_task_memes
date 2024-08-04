from unittest.mock import MagicMock

from app.core.mem.domain.image_repository import ImageRepository
from app.core.mem.domain.mem_repository import MemRepository


def get_mock_mem_repository():
    """
    Создаёт заглушку репозитория для мемов.
    """
    return MagicMock(spec=MemRepository)


def get_mock_image_repository():
    """
    Создаёт заглушку репозитория для картинок.
    """
    return MagicMock(spec=ImageRepository)


