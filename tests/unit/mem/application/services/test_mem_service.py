"""
Юнит-тесты сервиса мемов MemService.
"""
from unittest.mock import MagicMock
from uuid import UUID

from app.core.mem.application.schemas.mem_create_schema import MemCreateSchema
from app.core.mem.application.schemas.mem_read_schema import MemReadSchema
from app.core.mem.application.schemas.mem_update_schema import MemUpdateSchema
from app.core.mem.application.services.mem_service import MemService
from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID
from app.core.mem.infrastructure.models.mem_dao import MemDao
from tests.unit.mem.application.conftest import get_mock_mem_repository


class TestMemService:
    """
    Юнит-тесты для сервиса мемов :class:`MemService`
    """

    async def test_add_mem_should_return_mem(self):
        """
        Проверяет добавление мема через сервис и возвращение добавленного мема.
        """
        mock_mem_repository = get_mock_mem_repository()

        mem_to_add = MemCreateSchema(text='Колобок повесился.')
        mem_service = MemService(mock_mem_repository)
        added_mem = await mem_service.add_mem(mem_to_add)

        assert isinstance(added_mem, MemReadSchema)
        assert isinstance(added_mem.uuid, UUID)
        assert added_mem.text == 'Колобок повесился.'

    async def test_get_mem_by_id_should_return_mem(self):
        """
        Проверяет получение мема по идентификатору.
        """
        mock_mem = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                       text=MemText('Колобок повесился.'))
        mock_mem_repository = get_mock_mem_repository()
        mock_mem_repository.get_by_id.return_value = mock_mem

        mem_service = MemService(mock_mem_repository)
        mem = await mem_service.get_mem_by_id(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))

        assert isinstance(mem, MemReadSchema)
        assert mem.uuid == UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')
        assert mem.text == 'Колобок повесился.'

    async def test_get_all_memes_should_return_list_of_memes(self):
        """
        Проверяет получение списка всех мемов.
        """
        mock_memes = [
            Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                text=MemText('Колобок повесился.')),
            Mem(uuid=MemUUID(UUID('262f8c19-27c0-4e3c-b096-f6147ac052a3')),
                text=MemText('Купец.'))
        ]
        mock_mem_repository = get_mock_mem_repository()
        mock_mem_repository.get_all.return_value = mock_memes

        mem_service = MemService(mock_mem_repository)
        memes = await mem_service.get_all_memes()

        assert isinstance(memes, list)
        for mock_mem, mem in zip(mock_memes, memes):
            assert mem.uuid == mock_mem.uuid.uuid
            assert mem.text == mock_mem.text.text

    async def test_update_mem_should_return_mem(self):
        """
        Проверяет обновление мема через сервис и возвращение обновлённого мема.
        """
        mock_mem = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                       text=MemText('Колобок повесился.'))
        mock_mem_repository = get_mock_mem_repository()
        mock_mem_repository.update.return_value = mock_mem

        mem_to_update = MemUpdateSchema(uuid=UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'),
                                        text='Колобок повесился.')
        mem_service = MemService(mock_mem_repository)
        updated_mem = await mem_service.update_mem(mem_to_update)

        assert isinstance(updated_mem, MemReadSchema)
        assert updated_mem.uuid == UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')
        assert updated_mem.text == 'Колобок повесился.'
