"""
Юнит-тесты сущности Mem.
"""

from uuid import UUID

from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID


class TestMem:
    """
    Юнит-тесты для сущности :class:`Mem`
    """

    def test_create_entity_mem(self):
        """
        Проверяет корректное создание сущности мема.
        """
        mem = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                  text=MemText('Колобок повесился.'))

        assert mem.text == MemText('Колобок повесился.')
        assert mem.uuid == MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))

    def test_mem_identified_by_id(self):
        """
        Проверяет равенство мемов по их идентификаторам.
        """
        mem1 = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                   text=MemText('Колобок повесился.'))
        mem2 = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                   text=MemText('Колобок *********.'))
        mem3 = Mem(uuid=MemUUID(UUID('262f8c19-27c0-4e3c-b096-f6147ac052a3')),
                   text=MemText('Колобок повесился.'))

        assert mem1 == mem2
        assert mem1 != mem3
