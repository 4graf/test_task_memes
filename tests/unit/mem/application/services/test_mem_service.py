"""
Юнит-тесты сервиса мемов MemService.
"""
from io import BytesIO
from uuid import UUID

import pytest

from app.core.mem.application.exceptions import MemNotFoundException
from app.core.mem.application.schemas.mem_create_schema import MemCreateSchema
from app.core.mem.application.schemas.mem_read_schema import MemReadSchema
from app.core.mem.application.schemas.mem_update_schema import MemUpdateSchema
from app.core.mem.application.services.mem_service import MemService
from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.utils.mem_filter_params import MemFilterParams
from app.core.mem.domain.value_objects.image_path import ImagePath
from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID
from app.core.shared_kernel.db.exceptions import EntityNotFoundException
from tests.unit.mem.application.conftest import get_mock_mem_repository, get_mock_image_repository


class TestMemService:
    """
    Юнит-тесты для сервиса мемов :class:`MemService`
    """

    async def test_add_mem_without_image_should_return_mem(self):
        """
        Проверяет добавление мема без картинки через сервис и возвращение добавленного мема.
        """
        mock_mem_repository = get_mock_mem_repository()
        mock_image_repository = get_mock_image_repository()

        mem_to_add = MemCreateSchema(text='Колобок повесился.')
        mem_service = MemService(mock_mem_repository, mock_image_repository)
        added_mem = await mem_service.add_mem(mem_to_add)

        assert isinstance(added_mem, MemReadSchema)
        assert isinstance(added_mem.uuid, UUID)
        assert added_mem.text == 'Колобок повесился.'
        assert added_mem.image_path is None

    async def test_add_mem_with_image_should_return_mem(self):
        """
        Проверяет добавление мема с картинкой через сервис и возвращение добавленного мема.
        """
        mock_mem_repository = get_mock_mem_repository()
        mock_image_repository = get_mock_image_repository()

        mem_to_add = MemCreateSchema(text='Колобок повесился.')
        image_stream = BytesIO(b'meme_image')
        mem_service = MemService(mock_mem_repository, mock_image_repository)
        added_mem = await mem_service.add_mem(mem_to_add, image_stream)

        assert isinstance(added_mem, MemReadSchema)
        assert isinstance(added_mem.uuid, UUID)
        assert added_mem.text == 'Колобок повесился.'
        assert isinstance(added_mem.image_path, str)

    async def test_get_mem_by_id_should_return_mem(self):
        """
        Проверяет получение мема по идентификатору.
        """
        mock_mem = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                       text=MemText('Колобок повесился.'),
                       image_path=ImagePath('mem_777a3f52-ce9a-4758-a4d4-881221f94f63'))
        mock_mem_repository = get_mock_mem_repository()
        mock_mem_repository.get_by_id.return_value = mock_mem
        mock_image_repository = get_mock_image_repository()

        mem_service = MemService(mock_mem_repository, mock_image_repository)
        mem = await mem_service.get_mem_by_id(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))

        assert isinstance(mem, MemReadSchema)
        assert mem.uuid == UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')
        assert mem.text == 'Колобок повесился.'
        assert mem.image_path == 'mem_777a3f52-ce9a-4758-a4d4-881221f94f63'

    async def test_get_mem_image_should_return_bytes_stream(self):
        """
        Проверяет получение мема по идентификатору.
        """
        mock_mem_repository = get_mock_mem_repository()
        mock_image_repository = get_mock_image_repository()
        mock_image_repository.get_image.return_value = BytesIO(b'meme_image')

        mem_service = MemService(mock_mem_repository, mock_image_repository)
        image_stream = await mem_service.get_mem_image('mem_777a3f52-ce9a-4758-a4d4-881221f94f63')

        assert image_stream.getvalue() == BytesIO(b'meme_image').getvalue()

    async def test_get_all_memes_should_return_list_of_memes(self):
        """
        Проверяет получение списка всех мемов.
        """
        mock_memes = [
            Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                text=MemText('Колобок повесился.'),
                image_path=ImagePath('mem_777a3f52-ce9a-4758-a4d4-881221f94f63')),
            Mem(uuid=MemUUID(UUID('262f8c19-27c0-4e3c-b096-f6147ac052a3')),
                text=MemText('Купец.'),
                image_path=ImagePath('mem_262f8c19-27c0-4e3c-b096-f6147ac052a3'))
        ]
        mock_mem_repository = get_mock_mem_repository()
        mock_mem_repository.get_all.return_value = mock_memes
        mock_image_repository = get_mock_image_repository()

        mem_service = MemService(mock_mem_repository, mock_image_repository)
        mem_filter_params = MemFilterParams(page=1, per_page=2)
        memes = await mem_service.get_all_memes(mem_filter_params=mem_filter_params)

        assert isinstance(memes, list)
        for mem, mock_mem in zip(memes, mock_memes):
            assert mem.uuid == mock_mem.uuid.uuid
            assert mem.text == mock_mem.text.text
            assert mem.image_path == mock_mem.image_path.path

    async def test_update_mem_should_return_mem(self):
        """
        Проверяет обновление мема через сервис и возвращение обновлённого мема.
        """
        mock_mem = Mem(uuid=MemUUID(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')),
                       text=MemText('Колобок повесился.'),
                       image_path=ImagePath('mem_777a3f52-ce9a-4758-a4d4-881221f94f63'))
        mock_mem_repository = get_mock_mem_repository()
        mock_mem_repository.update.return_value = mock_mem
        mock_image_repository = get_mock_image_repository()

        mem_service = MemService(mock_mem_repository, mock_image_repository)
        mem_to_update = MemUpdateSchema(uuid=UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'),
                                        text='Колобок повесился.')
        updated_mem = await mem_service.update_mem(mem_to_update, BytesIO(b'meme_image'))

        assert isinstance(updated_mem, MemReadSchema)
        assert updated_mem.uuid == UUID('777a3f52-ce9a-4758-a4d4-881221f94f63')
        assert updated_mem.text == 'Колобок повесился.'
        assert updated_mem.image_path == 'mem_777a3f52-ce9a-4758-a4d4-881221f94f63'

    async def test_delete_not_exists_mem_should_raise_exception(self):
        """
        Проверяет обновление мема через сервис и возвращение обновлённого мема.
        """
        mock_mem_repository = get_mock_mem_repository()
        mock_mem_repository.delete_by_id.side_effect = EntityNotFoundException
        mock_image_repository = get_mock_image_repository()

        mem_service = MemService(mock_mem_repository, mock_image_repository)
        with pytest.raises(MemNotFoundException):
            await mem_service.delete_mem_by_id(UUID('777a3f52-ce9a-4758-a4d4-881221f94f63'))
