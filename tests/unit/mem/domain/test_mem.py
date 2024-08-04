"""
Юнит-тесты сущности Mem.
"""

from uuid import UUID

from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.value_objects.image_path import ImagePath
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
        mem1 = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                   text=MemText('Колобок повесился.'))
        mem2 = Mem(uuid=MemUUID(UUID('262f8c19-27c0-4e3c-b096-f6147ac052a3')),
                   text=MemText('Купец.'),
                   image_path=ImagePath('mem_262f8c19-27c0-4e3c-b096-f6147ac052a3'))

        assert mem1.text == MemText('Колобок повесился.')
        assert mem1.uuid == MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))
        assert mem1.image_path is None
        assert mem2.text == MemText('Купец.')
        assert mem2.uuid == MemUUID(UUID('262f8c19-27c0-4e3c-b096-f6147ac052a3'))
        assert mem2.image_path == ImagePath('mem_262f8c19-27c0-4e3c-b096-f6147ac052a3')

    def test_mem_identified_by_id(self):
        """
        Проверяет равенство мемов по их идентификаторам.
        """
        mem1 = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                   text=MemText('Колобок повесился.'))
        mem2 = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                   text=MemText('Колобок *********.'),
                   image_path=ImagePath('memas_777a3f52-ce9a-4758-a4d4-881221f94f63'))
        mem3 = Mem(uuid=MemUUID(UUID('262f8c19-27c0-4e3c-b096-f6147ac052a3')),
                   text=MemText('Колобок повесился.'))

        assert mem1 == mem2
        assert mem1 != mem3

    def test_upload_image_should_create_image_path(self):
        """
        Проверяет загрузку изображения и создание пути картинки.
        """
        mem = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                  text=MemText('Колобок повесился.'))

        assert mem.image_path is None

        mem.upload_image()
        assert mem.image_path == ImagePath('mem_777a3f52-ce9a-4758-a4d4-881221f94f63')

        mem.upload_image(ImagePath('memas_777a3f52-ce9a-4758-a4d4-881221f94f63'))
        assert mem.image_path == ImagePath('memas_777a3f52-ce9a-4758-a4d4-881221f94f63')
