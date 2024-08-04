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


class AuthenticationSettings(BaseSettings):
    """
    Настройки аутентификации.

    :cvar access_secret_key: Секретный ключ для генерации токенов доступа.
    :cvar access_expiration: Время жизни токенов доступа в минутах.
    :cvar refresh_secret_key: Секретный ключ для генерации токенов обновления.
    :cvar refresh_expiration: Время жизни токенов обновления в минутах.
    :cvar jwt_algorithm: Алгоритм кодирования токена.
    :cvar password_salt: Соль для хеширования пароля пользователя.
    :cvar iters_hashing: Количество итераций для хеширования пароля пользователя.
    :cvar hash_algorithm: Алгоритм для хеширования пароля пользователя.
    """

    access_secret_key: str
    access_expiration: int
    refresh_secret_key: str
    refresh_expiration: int
    jwt_algorithm: str
    password_salt: str
    iters_hashing: int
    hash_algorithm: str
