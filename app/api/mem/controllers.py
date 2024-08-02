"""
API-маршруты для работы с мемами.
"""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from app.api.http_errors import ResourceNotFoundError, ResourceExistsError, RequestParamValidationError
from app.api.mem.dependencies import get_mem_service
from app.api.mem.schemas.mem_update_request import MemUpdateRequest
from app.core.mem.application.exceptions import MemNotFoundException, MemExistsException
from app.core.mem.application.schemas.mem_create_schema import MemCreateSchema
from app.core.mem.application.schemas.mem_read_schema import MemReadSchema
from app.core.mem.application.schemas.mem_update_schema import MemUpdateSchema
from app.core.mem.application.services.mem_service import MemService
from app.core.mem.domain.exceptions.base_mem_exceptions import MemValidationException

mem_router = APIRouter(prefix='/memes', tags=['Mem'])


@mem_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[MemReadSchema]
)
async def get_all_memes(mem_service: Annotated[MemService, Depends(get_mem_service)]) -> list[MemReadSchema]:
    """
    Маршрут для получения всех мемов.

    :param mem_service: Сервис для работы с мемами.
    :return: Список мемов.
    """
    memes = await mem_service.get_all_memes()
    return memes


@mem_router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=MemReadSchema
)
async def get_mem_by_id(id: UUID,
                        mem_service: Annotated[MemService, Depends(get_mem_service)]) -> MemReadSchema:
    """
    Маршрут для получения мема по его идентификатору.

    :param id: Уникальный идентификатор мема.
    :param mem_service: Сервис для работы с мемами.
    :return: Мем.
    """
    try:
        mem = await mem_service.get_mem_by_id(id)
    except MemNotFoundException as exc:
        raise ResourceNotFoundError(exception_msg=str(exc)) from exc
    return mem


@mem_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=MemReadSchema
)
async def add_mem(mem_to_add: MemCreateSchema,
                  mem_service: Annotated[MemService, Depends(get_mem_service)]) -> MemReadSchema:
    """
    Маршрут для добавления мема.

    :param mem_to_add: Информация о меме.
    :param mem_service: Сервис для работы с мемами.
    :return: Добавленный мем.
    """
    try:
        added_mem = await mem_service.add_mem(mem_to_add)
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
                     mem_to_update: MemUpdateRequest,
                     mem_service: Annotated[MemService, Depends(get_mem_service)]) -> MemReadSchema:
    """
    Маршрут для обновления мема по его идентификатору.

    :param id: Уникальный идентификатор мема.
    :param mem_to_update: Новая информация о меме.
    :param mem_service: Сервис для работы с мемами.
    :return: Обновлённый мем.
    """
    try:
        mem_to_update_internal = MemUpdateSchema(uuid=id,
                                                 text=mem_to_update.text)
        updated_mem = await mem_service.update_mem(mem_to_update_internal)
    except MemValidationException as exc:
        raise RequestParamValidationError(exception_msg=str(exc)) from exc
    except MemExistsException as exc:
        raise ResourceExistsError(exception_msg=str(exc)) from exc
    return updated_mem


@mem_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_mem_by_id(id: UUID,
                           mem_service: Annotated[MemService, Depends(get_mem_service)]) -> None:
    """
    Маршрут для удаления мема по его идентификатору.

    :param id: Уникальный идентификатор мема.
    :param mem_service: Сервис для работы с мемами.
    """
    await mem_service.delete_mem_by_id(id)
