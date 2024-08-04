"""
Функции для получения зависимостей базы данных.
Включает в себя создание асинхронной сессии БД.
"""
import boto3
from mypy_boto3_s3 import ServiceResource
from mypy_boto3_s3.service_resource import Bucket
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.settings import DatabaseSettings, ImageStorageSettings

db_settings = DatabaseSettings()
image_storage_settings = ImageStorageSettings()

engine = create_async_engine(db_settings.postgres_url.unicode_string(), echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_db_session() -> AsyncSession:
    """
    Получает асинхронную сессию для взаимодействия с базой данных.

    :return: Асинхронная сессия SQLAlchemy.
    """

    async with async_session_maker() as session:
        try:
            yield session
        except Exception:
            ...
            await session.rollback()
            raise
        finally:
            await session.close()


def get_s3_resource() -> ServiceResource:
    return boto3.resource(service_name='s3',
                          endpoint_url=db_settings.s3_storage_url,
                          aws_access_key_id=db_settings.s3_access_key_id,
                          aws_secret_access_key=db_settings.s3_secret_access_key,
                          region_name='ru-central1')


def get_s3_bucket_image() -> Bucket:

    s3_resource = get_s3_resource()
    bucket = s3_resource.Bucket(image_storage_settings.bucket_name)

    return bucket
