"""
Функции для получения зависимостей мемов.
Включает в себя создание сервиса мемов.
"""

from fastapi import Depends
from mypy_boto3_s3.service_resource import Bucket
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.mem.application.services.mem_service import MemService
from app.core.mem.infrastructure.repositories.image_repository import ImageS3Repository
from app.core.mem.infrastructure.repositories.mem_repository import MemDBRepository
from app.core.shared_kernel.db.dependencies import get_async_db_session, get_s3_bucket_image


async def get_mem_service(session: AsyncSession = Depends(get_async_db_session),
                          bucket: Bucket = Depends(get_s3_bucket_image)) -> MemService:
    """
    Получает сервис мемов.

    :param session: Асинхронная сессия базы данных.
    :param bucket: Бакет картинок мемов в S3 хранилище.
    :return: Сервис мемов.
    """

    mem_repository = MemDBRepository(session)
    image_repository = ImageS3Repository(bucket)
    return MemService(mem_repository=mem_repository, image_repository=image_repository)
