"""
API-маршруты для работы с мемами.
"""
import base64
from io import BytesIO
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import Response
from starlette import status

from app.api.helpers.user_helper import UserHelper
from app.api.http_errors import ResourceNotFoundError, ResourceExistsError, RequestParamValidationError
from app.api.mem.dependencies import get_mem_service
from app.api.mem.schemas.mem_read_response import MemReadResponse
from app.api.mem.schemas.mem_update_request import MemUpdateRequest
from app.api.shared_dependencies import get_current_user_role
from app.core.mem.application.exceptions import MemNotFoundException, MemExistsException
from app.core.mem.application.schemas.mem_create_schema import MemCreateSchema
from app.core.mem.application.schemas.mem_read_schema import MemReadSchema
from app.core.mem.application.schemas.mem_update_schema import MemUpdateSchema
from app.core.mem.application.services.mem_service import MemService
from app.core.mem.domain.exceptions.base_mem_exceptions import MemValidationException
from app.core.mem.domain.utils.mem_filter_params import MemFilterParams
from app.core.user.application.authentication.schemas.user_from_token_schema import UserFromTokenSchema

mem_router = APIRouter(prefix='/memes', tags=['Mem'])


@mem_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[MemReadSchema]
)
async def get_all_memes(mem_service: Annotated[MemService, Depends(get_mem_service)],
                        mem_filter_params: MemFilterParams = Depends()) -> list[MemReadSchema]:
    """
    Маршрут для получения всех мемов.

    :param mem_filter_params: Параметры фильтрации мемов.
    :param mem_service: Сервис для работы с мемами.
    :return: Список мемов.
    """
    memes = await mem_service.get_all_memes(mem_filter_params=mem_filter_params)
    return memes


@mem_router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=MemReadResponse
)
async def get_mem_by_id(id: UUID,
                        mem_service: Annotated[MemService, Depends(get_mem_service)]) -> MemReadResponse:
    """
    Маршрут для получения мема по его идентификатору.

    :param id: Уникальный идентификатор мема.
    :param mem_service: Сервис для работы с мемами.
    :return: Мем.
    """
    try:
        mem = await mem_service.get_mem_by_id(id)
        if mem.image_path:
            with await mem_service.get_mem_image(mem.image_path) as image_stream:
                image_bytes = base64.b64encode(image_stream.getvalue())
        else:
            image_bytes = None
    except MemNotFoundException as exc:
        raise ResourceNotFoundError(exception_msg=str(exc)) from exc

    response_mem = MemReadResponse(mem=mem,
                                   image_bytes=image_bytes)
    return response_mem


@mem_router.get(
    "/{id}/image",
    status_code=status.HTTP_200_OK,
)
async def get_mem_image(id: UUID,
                        mem_service: Annotated[MemService, Depends(get_mem_service)]) -> Response:
    """
    Маршрут для получения картинки мема по его идентификатору.

    :param id: Уникальный идентификатор мема.
    :param mem_service: Сервис для работы с мемами.
    :return: Картинка мема.
    """
    try:
        mem = await mem_service.get_mem_by_id(id)
    except MemNotFoundException as exc:
        raise ResourceNotFoundError(exception_msg=str(exc)) from exc

    if not mem.image_path:
        raise ResourceNotFoundError

    with await mem_service.get_mem_image(mem.image_path) as image_stream:
        return Response(content=image_stream.getvalue(), media_type="image/png")


@mem_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=MemReadSchema
)
async def add_mem(mem_to_add: Annotated[MemCreateSchema, Depends()],
                  current_user_role: Annotated[UserFromTokenSchema, Depends(get_current_user_role)],
                  mem_service: Annotated[MemService, Depends(get_mem_service)],
                  image_file: UploadFile = None) -> MemReadSchema:
    """
    Маршрут для добавления мема.

    :param mem_to_add: Информация о меме.
    :param current_user_role: Роль текущего пользователя.
    :param mem_service: Сервис для работы с мемами.
    :param image_file: Картинка мема.
    :return: Добавленный мем.
    """
    UserHelper.assert_is_admin(current_user_role)

    # Проверку на размер файла надо бы иметь на веб-сервере
    if image_file:
        if image_file.size > 8 * 2**20:
            raise RequestParamValidationError(
                exception_msg='Изображение слишком большое. Поддерживаются изображения до 8 Мб.'
            )
        image_stream = BytesIO(await image_file.read())
    else:
        image_stream = None

    try:
        added_mem = await mem_service.add_mem(mem_to_add, image_stream)
    except MemValidationException as exc:
        raise RequestParamValidationError(exception_msg=str(exc)) from exc
    except MemExistsException as exc:
        raise ResourceExistsError(exception_msg=str(exc)) from exc
    return added_mem


@mem_router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=MemReadSchema
)
async def update_mem(id: UUID,
                     mem_to_update: Annotated[MemUpdateRequest, Depends()],
                     current_user_role: Annotated[UserFromTokenSchema, Depends(get_current_user_role)],
                     mem_service: Annotated[MemService, Depends(get_mem_service)],
                     image_file: UploadFile = None) -> MemReadSchema:
    """
    Маршрут для обновления мема по его идентификатору.

    :param id: Уникальный идентификатор мема.
    :param mem_to_update: Новая информация о меме.
    :param current_user_role: Роль текущего пользователя.
    :param mem_service: Сервис для работы с мемами.
    :param image_file: Картинка мема.
    :return: Обновлённый мем.
    """
    UserHelper.assert_is_admin(current_user_role)

    # Проверку на размер файла надо бы иметь на веб-сервере
    if image_file:
        if image_file.size > 8 * 2**20:
            raise RequestParamValidationError(
                exception_msg='Изображение слишком большое. Поддерживаются изображения до 8 Мб.'
            )
        image_stream = BytesIO(await image_file.read())
    else:
        image_stream = None

    try:
        mem_to_update_internal = MemUpdateSchema(uuid=id,
                                                 text=mem_to_update.text)
        updated_mem = await mem_service.update_mem(mem_to_update_internal, image_stream)
    except MemValidationException as exc:
        raise RequestParamValidationError(exception_msg=str(exc)) from exc
    except MemNotFoundException as exc:
        raise ResourceNotFoundError(exception_msg=str(exc)) from exc
    except MemExistsException as exc:
        raise ResourceExistsError(exception_msg=str(exc)) from exc
    return updated_mem


@mem_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_mem_by_id(id: UUID,
                           current_user_role: Annotated[UserFromTokenSchema, Depends(get_current_user_role)],
                           mem_service: Annotated[MemService, Depends(get_mem_service)]) -> None:
    """
    Маршрут для удаления мема по его идентификатору.

    :param id: Уникальный идентификатор мема.
    :param current_user_role: Роль текущего пользователя.
    :param mem_service: Сервис для работы с мемами.
    """
    UserHelper.assert_is_admin(current_user_role)

    try:
        await mem_service.delete_mem_by_id(id)
    except MemValidationException as exc:
        raise RequestParamValidationError(exception_msg=str(exc)) from exc
    except MemNotFoundException as exc:
        raise ResourceNotFoundError(exception_msg=str(exc)) from exc
