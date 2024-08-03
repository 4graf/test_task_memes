"""
Юнит-тесты объекта значения MemUUID.
"""

from uuid import UUID

import pytest

from app.core.mem.domain.exceptions.base_mem_exceptions import MemTypeError
from app.core.mem.domain.value_objects.mem_uuid import MemUUID


class TestMemUUID:
    """
    Юнит-тесты для объекта значения :class:`MemUUID`
    """

    def test_create_valueobject_memuuid(self):
        """
        Проверяет корректное создание объекта значения идентификатора мема.
        """
        mem_uuid = MemUUID(uuid=UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))

        assert mem_uuid.uuid == UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')

    def test_uuid_non_uuid_type(self):
        """
        Проверяет выбрасывание исключения при попытке передачи некорректного типа данных для идентификатора мема.
        """
        uuid = '777a'
        with pytest.raises(MemTypeError):
            MemUUID(uuid=uuid)

    def test_memuuids_equality(self):
        """
        Проверяет равенство одинаковых идентификаторов мемов.
        """
        mem_uuid1 = MemUUID(uuid=UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))
        mem_uuid2 = MemUUID(uuid=UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))

        assert mem_uuid1 == mem_uuid2

    def test_memuuids_inequality(self):
        """
        Проверяет неравенство разных идентификаторов мемов.
        """
        mem_uuid1 = MemUUID(uuid=UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))
        mem_uuid2 = MemUUID(uuid=UUID('262f8c19-27c0-4e3c-b096-f6147ac052a3'))

        assert mem_uuid1 != mem_uuid2
