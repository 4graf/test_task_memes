"""
API-маршруты для управления пользователями.
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from app.api.helpers.user_helper import UserHelper
from app.api.http_errors import ResourceNotFoundError, ResourceExistsError, RequestParamValidationError
from app.api.shared_dependencies import get_current_user_role
from app.api.users.dependencies import get_user_service
from app.core.user.application.authentication.schemas.user_from_token_schema import UserFromTokenSchema
from app.core.user.application.user.exceptions import UserNotFoundException, UserExistsException
from app.core.user.application.user.schemas.user_read_schema import UserReadSchema
from app.core.user.application.user.schemas.user_update_schema import UserUpdateSchema
from app.core.user.application.user.services.user_service import UserService
from app.core.user.domain.exceptions.base_user_exceptions import UserValidationException

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.get("/all", status_code=status.HTTP_200_OK)
async def get_users(current_user_role: Annotated[UserFromTokenSchema, Depends(get_current_user_role)],
                    user_service: Annotated[UserService, Depends(get_user_service)]) \
        -> list[UserReadSchema]:
    """
    Получает всех пользователей

    :param current_user_role: Роль текущего пользователя.
    :param user_service: Сервис для работы с пользователями.
    :return: Данные пользователя.
    """
    UserHelper.assert_is_admin(current_user_role)

    return await user_service.get_all_user()


@user_router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(current_user_role: Annotated[UserFromTokenSchema, Depends(get_current_user_role)],
                 user_service: Annotated[UserService, Depends(get_user_service)]) \
        -> UserReadSchema:
    """
    Получает текущего пользователя.

    :param current_user_role: Роль текущего пользователя.
    :param user_service: Сервис для работы с пользователями.
    :return: Данные пользователя.
    """
    try:
        user = await user_service.get_user_by_id(current_user_role.uuid)
    except UserNotFoundException as e:
        raise ResourceNotFoundError(exception_msg=str(e)) from e

    return user


@user_router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=UserReadSchema
)
async def update_user(user_to_update: UserUpdateSchema,
                      current_user_role: Annotated[UserFromTokenSchema, Depends(get_current_user_role)],
                      user_service: Annotated[UserService, Depends(get_user_service)]) \
        -> UserReadSchema:
    """
    Обновляет пользователя по его идентификатору.

    :param user_to_update: Данные пользователя для обновления.
    :param current_user_role: Роль текущего пользователя.
    :param user_service: Сервис для работы с пользователями.
    :return: Данные пользователя.
    """
    UserHelper.assert_is_admin(current_user_role)

    try:
        user = await user_service.update_user(user_to_update)
    except UserValidationException as exc:
        raise RequestParamValidationError(exception_msg=str(exc)) from exc
    except UserNotFoundException as exc:
        raise ResourceNotFoundError(exception_msg=str(exc)) from exc
    except UserExistsException as exc:
        raise ResourceExistsError(exception_msg=str(exc)) from exc

    return user
