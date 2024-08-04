"""
Сервис для работы с мемами MemService.
"""
from io import BytesIO
from uuid import uuid4, UUID

from app.core.mem.application.exceptions import MemNotFoundException, MemExistsException
from app.core.mem.application.schemas.mem_create_schema import MemCreateSchema
from app.core.mem.application.schemas.mem_read_schema import MemReadSchema
from app.core.mem.application.schemas.mem_update_schema import MemUpdateSchema
from app.core.mem.domain.image_repository import ImageRepository
from app.core.mem.domain.mem_entity import Mem
from app.core.mem.domain.mem_repository import MemRepository
from app.core.mem.domain.utils.mem_filter_params import MemFilterParams
from app.core.mem.domain.value_objects.mem_text import MemText
from app.core.mem.domain.value_objects.mem_uuid import MemUUID
from app.core.shared_kernel.db.exceptions import EntityExistsException, EntityNotFoundException


class MemService:
    """
    Сервис для работы с мемами.

    :ivar mem_repository: Репозиторий мемов.
    """

    def __init__(self, mem_repository: MemRepository, image_repository: ImageRepository):
        """
        Конструктор MemService.

        :param mem_repository: Репозиторий мемов.
        :param image_repository: Репозиторий картинок мемов.
        """
        self.mem_repository = mem_repository
        self.image_repository = image_repository

    async def add_mem(self, data: MemCreateSchema, image_stream: BytesIO = None) -> MemReadSchema:
        """
        Добавляет новый мем.

        :param data: Данные для создания мема.
        :param image_stream: Двоичный поток с данными изображения.
        :return: Информация созданного мема.
        :raise MemExistsException: Добавление мема, который уже существует.
        """
        mem = Mem(
            uuid=MemUUID(uuid4()),
            text=MemText(data.text)
        )
        if image_stream:
            mem.upload_image()
            self.image_repository.save_image(path=mem.image_path.path, image_stream=image_stream)
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

    async def get_mem_image(self, path: str) -> BytesIO:
        """
        Получает картинку меме по пути.

        :param path: Путь к картинке мема.
        :return: Бинарный поток с картинкой мема.
        """

        return self.image_repository.get_image(path=path)

    async def get_all_memes(self, mem_filter_params: MemFilterParams) -> list[MemReadSchema]:
        """
        Получает информацию о меме по его идентификатору.

        :return: Список с информациями о мемах.
        """
        memes = await self.mem_repository.get_by_filter(mem_filter_params=mem_filter_params)
        return [MemReadSchema.from_entity(mem) for mem in memes]

    async def update_mem(self, data: MemUpdateSchema, image_stream: BytesIO = None) -> MemReadSchema:
        """
        Обновляет мем.

        :param data: Данные для обновления мема.
        :param image_stream: Двоичный поток с данными изображения.
        :return: Информация обновленного мема.
        :raise MemExistsException: Добавление мема, который уже существует.
        """
        new_mem = Mem(
            uuid=MemUUID(data.uuid),
            text=MemText(data.text)
        )
        try:
            old_mem = await self.mem_repository.get_by_id(data.uuid)
            if old_mem.image_path:
                self.image_repository.delete_image(old_mem.image_path.path)

            if image_stream:
                new_mem.upload_image()
                self.image_repository.save_image(path=new_mem.image_path.path, image_stream=image_stream)

            await self.mem_repository.update(new_mem)
        except EntityNotFoundException as e:
            raise MemNotFoundException from e
        except EntityExistsException as e:
            raise MemExistsException from e

        return MemReadSchema.from_entity(new_mem)

    async def delete_mem_by_id(self, id_: UUID) -> None:
        """
        Удаляет мем по его идентификатору.

        :param id_: Уникальный идентификатор мема.
        """

        try:
            mem = await self.mem_repository.get_by_id(id_)
            await self.mem_repository.delete_by_id(id_)
            if mem.image_path:
                self.image_repository.delete_image(mem.image_path.path)
        except EntityNotFoundException as e:
            raise MemNotFoundException from e
