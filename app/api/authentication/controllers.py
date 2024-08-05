"""
API-маршруты для аутентификации.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api.authentication.dependencies import get_authentication_service
from app.api.http_errors import ResourceExistsError, RequestParamValidationError, AuthenticationUserError
from app.core.user.application.authentication.exceptions import AuthenticationException
from app.core.user.application.authentication.schemas.access_token_schema import AccessTokenSchema
from app.core.user.application.authentication.schemas.user_login_schema import UserLoginSchema
from app.core.user.application.authentication.schemas.user_register_schema import UserRegisterSchema
from app.core.user.application.authentication.services.authentication_service import AuthenticationService
from app.core.user.application.user.exceptions import UserExistsException, UserNotFoundException
from app.core.user.domain.exceptions.base_user_exceptions import UserException

authentication_router = APIRouter(prefix='/auth', tags=['Authentication'])


@authentication_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=AccessTokenSchema
)
async def register_user(user: UserRegisterSchema,
                        authentication_service: Annotated[AuthenticationService, Depends(get_authentication_service)],
                        response: Response) \
        -> AccessTokenSchema:
    """
    Маршрут для регистрации нового пользователя

    :param user: Данные нового пользователя.
    :param authentication_service: Сервис для работы с аутентификацией.
    :param response: Объект ответа для установления cookies.
    :return: Пара токенов доступа и обновления.
    """
    try:
        tokens = await authentication_service.register_user(data=user)
    except UserExistsException as e:
        raise ResourceExistsError(exception_msg=str(e)) from e
    except UserException as e:
        raise RequestParamValidationError(exception_msg=str(e)) from e

    response.set_cookie(key='refresh_token',
                        value=tokens.refresh_token.refresh_token,
                        httponly=True,
                        samesite='lax')
    access_token = tokens.access_token
    return access_token


@authentication_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=AccessTokenSchema
)
async def login(authentication_service: Annotated[AuthenticationService, Depends(get_authentication_service)],
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                response: Response) \
        -> AccessTokenSchema:
    """
    Маршрут для авторизации пользователя.

    :param authentication_service: Сервис для работы с аутентификацией.
    :param form_data: Данные для аутентификации пользователя.
    :param response: Объект ответа для установления cookies.
    :return: Пара токенов доступа и обновления.
    """
    try:
        user_login = UserLoginSchema(login=form_data.username,
                                     password=form_data.password)
        tokens = await authentication_service.login(user_login=user_login)
    except (UserNotFoundException, AuthenticationException) as e:
        raise AuthenticationUserError(exception_msg=str(e)) from e

    response.set_cookie(key='refresh_token',
                        value=tokens.refresh_token.refresh_token,
                        httponly=True,
                        samesite='lax')
    access_token = tokens.access_token
    return access_token


@authentication_router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(authentication_service: Annotated[AuthenticationService, Depends(get_authentication_service)],
                  response: Response,
                  refresh_token: Annotated[str | None, Cookie()] = None) \
        -> AccessTokenSchema:
    """
    Обновляет токены доступа и обновления пользователя

    :param authentication_service: Сервис для работы с аутентификацией.
    :param response: Объект ответа для установления cookies.
    :param refresh_token: Токен обновления пользователя из куки.
    :return: Пара токенов доступа и обновления.
    """
    if not refresh_token:
        raise AuthenticationUserError(msg='Refresh token not found, login again.')
    try:
        tokens = await authentication_service.refresh(refresh_token)
    except (UserNotFoundException, AuthenticationException) as e:
        raise AuthenticationUserError(exception_msg=str(e)) from e

    response.set_cookie(key='refresh_token',
                        value=tokens.refresh_token.refresh_token,
                        httponly=True,
                        samesite='lax')
    access_token = tokens.access_token
    return access_token
