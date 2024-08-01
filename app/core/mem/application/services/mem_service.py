"""
Сервис для работы с мемами MemService.
"""

from uuid import uuid4, UUID

from app.core.mem.application.exceptions import MemNotFoundException, MemExistsException
from app.core.mem.application.schemas.mem_create_schema import MemCreateSchema
from app.core.mem.application.schemas.mem_read_schema import MemReadSchema
from app.core.mem.application.schemas.mem_update_schema import MemUpdateSchema
from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.mem_repository import MemRepository
from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID
from app.core.shared_kernel.db.exceptions import EntityExistsException


class MemService:
    """
    Сервис для работы с мемами.

    :ivar mem_repository: Репозиторий мемов.
    """

    def __init__(self, mem_repository: MemRepository):
        """
        Конструктор MemService.

        :param mem_repository: Репозиторий мемов.
        """
        self.mem_repository = mem_repository

    async def add_mem(self, data: MemCreateSchema) -> MemReadSchema:
        """
        Добавляет новый мем.

        :param data: Данные для создания мема.
        :return: Информация созданного мема.
        :raise MemExistsException: Добавление мема, который уже существует.
        """

        mem = Mem(
            uuid=MemUUID(uuid4()),
            text=MemText(data.text)
        )
        try:
            await self.mem_repository.add(mem)
        except EntityExistsException as e:
            raise MemExistsException from e

        return MemReadSchema.from_entity(mem)

    async def get_mem_by_id(self, id_: UUID) -> MemReadSchema:
        """
        Получает информацию о меме по его идентификатору.

        :param id_: Уникальный идентификатор мема.
        :return: Информация о меме.
        :raise MemNotFoundException: Мем не был найден.
        """
        mem = await self.mem_repository.get_by_id(id_)
        if not mem:
            raise MemNotFoundException
        return MemReadSchema.from_entity(mem)

    async def get_all_memes(self) -> list[MemReadSchema]:
        """
        Получает информацию о меме по его идентификатору.

        :return: Список с информациями о мемах.
        """
        memes = await self.mem_repository.get_all()
        return [MemReadSchema.from_entity(mem) for mem in memes]

    async def update_mem(self, data: MemUpdateSchema) -> MemReadSchema:
        """
        Обновляет мем.

        :param data: Данные для обновления мема.
        :return: Информация обновленного мема.
        :raise MemExistsException: Добавление мема, который уже существует.
        """

        mem = Mem(
            uuid=MemUUID(data.uuid),
            text=MemText(data.text)
        )
        try:
            await self.mem_repository.update(mem)
        except EntityExistsException as e:
            raise MemExistsException from e

        return MemReadSchema.from_entity(mem)

    async def delete_mem_by_id(self, id_: UUID) -> None:
        """
        Удаляет мем по его идентификатору.

        :param id_: Уникальный идентификатор мема.
        """

        await self.mem_repository.delete_by_id(id_)
