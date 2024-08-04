"""
Юнит-тесты объекта значения ImagePath.
"""

import pytest

from app.core.mem.domain.exceptions.base_mem_exceptions import MemTypeError
from app.core.mem.domain.value_objects.image_path import ImagePath
from app.core.mem.domain.value_objects.mem_text import MemText


class TestImagePath:
    """
    Юнит-тесты для объекта значения :class:`ImagePath`
    """

    def test_create_valueobject_imagepath(self):
        """
        Проверяет корректное создание объекта значения пути картинки.
        """
        image_path = ImagePath('mem_777a3f52-ce9a-4758-a4d4-881221f94f63')

        assert image_path.path == 'mem_777a3f52-ce9a-4758-a4d4-881221f94f63'

    def test_path_non_str_type(self):
        """
        Проверяет выбрасывание исключения при попытке передачи некорректного типа данных для пути картинки.
        """
        path = 322
        with pytest.raises(MemTypeError):
            ImagePath(path=path)

    def test_imagepaths_equality(self):
        """
        Проверяет равенство одинаковых путей к картинкам.
        """
        path = 'mem_777a3f52-ce9a-4758-a4d4-881221f94f63'
        image_path1 = ImagePath(path)
        image_path2 = ImagePath(path)

        assert image_path1 == image_path2

    def test_memtexts_inequality(self):
        """
        Проверяет неравенство разных текстов мемов.
        """
        image_path1 = ImagePath('mem_777a3f52-ce9a-4758-a4d4-881221f94f63')
        image_path2 = ImagePath('mem_262f8c19-27c0-4e3c-b096-f6147ac052a3')

        assert image_path1 != image_path2
