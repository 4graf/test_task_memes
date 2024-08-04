"""
Настройки проекта.
"""

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DatabaseSettings(BaseSettings):
    """
    Настройки для работы с базой данных.

    :cvar postgres_url: Url подключения к PostgreSQL.
    """
    postgres_url: PostgresDsn
    s3_storage_url: str
    s3_access_key_id: str
    s3_secret_access_key: str


class ImageStorageSettings(BaseSettings):
    """
    Настройки для работы с S3 хранилищем с изображенями.

    :cvar bucket_name: Имя бакета с изображениями.
    """
    model_config = SettingsConfigDict(env_prefix='images_')

    bucket_name: str
