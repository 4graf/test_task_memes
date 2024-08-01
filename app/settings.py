"""
Настройки проекта.
"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DatabaseSettings(BaseSettings):
    """
    Настройки для работы с базой данных.

    :cvar postgresql_url: Url подключения к PostgreSQL.
    """

    postgresql_url: str
