from unittest.mock import MagicMock

from app.core.mem.domain.mem_repository import MemRepository


def get_mock_mem_repository():
    """
    Создаёт заглушку репозитория базы данных.
    """
    return MagicMock(spec=MemRepository)
