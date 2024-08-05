"""
Класс-помощник для пользователя.
"""
from app.api.http_errors import AccessRightsError
from app.core.shared_kernel.domain.value_objects.user_role import UserRole
from app.core.user.application.authentication.schemas.user_from_token_schema import UserFromTokenSchema


class UserHelper:
    """
    Класс-помощник для пользователя.
    """
    @staticmethod
    def assert_is_admin(current_user: UserFromTokenSchema, exception_message: str = None) -> None:
        """
        Проверяет роль текущего пользователя на администратора.
        :param current_user: Текущий пользователь.
        :param exception_message: Сообщение для исключения при возникновении ошибки.
        """
        if current_user.role != UserRole.ADMIN:
            if not exception_message:
                exception_message = "Действие доступно только администраторам."
            raise AccessRightsError(exception_msg=exception_message)
