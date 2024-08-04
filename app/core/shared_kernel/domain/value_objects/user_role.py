"""
Перечисление ролей пользователей.
"""
from enum import Enum


class UserRole(Enum):
    """
    Перечисление ролей пользователей.
    """
    ADMIN = "ADMIN"
    CLIENT = "CLIENT"
