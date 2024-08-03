"""
Юнит-тесты модели DAO MemDao.
"""
from uuid import UUID

from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID
from app.core.mem.infrastructure.models.mem_dao import MemDao


class TestMemDao:
    """
    Юнит-тесты для модели DAO :class:`MemDao`
    """

    def test_to_dict_should_create_dict_with_columns_name_and_values(self):
        """
        Проверяет создание словаря из DAO мема, где ключ - название столбца, а значение - его значение столбца.
        """
        mem_dao = MemDao(id=UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'),
                         text='Колобок повесился.')

        assert mem_dao.to_dict() == {'id': UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'),
                                     'text': 'Колобок повесился.'}

    def test_to_entity_should_create_entity_instance(self):
        """
        Проверяет создание сущности мема из DAO мема.
        """
        mem_dao = MemDao(id=UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'),
                         text='Колобок повесился.')
        mem = mem_dao.to_entity()

        assert mem.uuid == MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))
        assert mem.text == MemText('Колобок повесился.')

    def test_from_entity_should_create_dao_instance(self):
        """
        Проверяет создание DAO мема из сущности мема.
        """
        mem = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                  text=MemText('Колобок повесился.'))
        mem_dao = MemDao.from_entity(mem)

        assert mem_dao.id == UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')
        assert mem_dao.text == 'Колобок повесился.'
