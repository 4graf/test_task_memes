"""
Настройки проекта.
"""

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

load_dotenv()


class DatabaseSettings(BaseSettings):
    """
    Настройки для работы с базой данных.

    :cvar postgres_url: Url подключения к PostgreSQL.
    """

    postgres_url: PostgresDsn
