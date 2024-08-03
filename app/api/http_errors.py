"""
HTTP-ошибки для API.
"""

from fastapi import HTTPException
from starlette import status


class ResourceNotFoundError(HTTPException):
    """
    Ошибка, возникающая при не нахождении ресурса.
    """

    def __init__(self, msg='Ресурс не был найден.', exception_msg=''):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail={"message": f"{msg}: {exception_msg}"})


class ResourceExistsError(HTTPException):
    """
    Ошибка, возникающая при добавлении уже существующего ресурса.
    """

    def __init__(self, msg='Ресурс уже существует.', exception_msg=''):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail={"message": f"{msg}: {exception_msg}"})


class RequestParamValidationError(HTTPException):
    """
    Ошибка валидации параметра запроса.
    """
    def __init__(self, msg='Ошибка валидации параметра.', exception_msg=''):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         detail={"message": f"{msg}: {exception_msg}"})
