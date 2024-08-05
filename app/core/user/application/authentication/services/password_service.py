"""
Сервис для работы с паролями пользователей.
"""
import hashlib

from app.settings import AuthenticationSettings

settings = AuthenticationSettings()


class PasswordService:
    """
    Сервис для работы с паролями пользователей.
    """
    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Хэширует пароль.
        :param password: Пароль.
        :return: Хэш пароля.
        """
        hashed = hashlib.pbkdf2_hmac(settings.hash_algorithm,
                                     password.encode(),
                                     settings.password_salt.encode(),
                                     settings.iters_hashing)
        return hashed.hex()

    @classmethod
    def validate_password(cls, login_password, hashed_password: str) -> bool:
        """
        Проверяет пароль с хэшом пароля на идентичность.
        :param login_password: Пароль
        :param hashed_password: Хэш пароля
        :return: True, если пароль соответствует хэшу, False иначе.
        """
        return cls.hash_password(login_password) == hashed_password
