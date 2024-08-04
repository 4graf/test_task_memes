"""
Интерфейс репозитория для работы с изображениями.
"""
from abc import ABC, abstractmethod
from io import BytesIO


class ImageRepository(ABC):
    """
    Интерфейс репозитория для изображений мемов.
    """

    @abstractmethod
    def save_image(self, path: str, image_stream: BytesIO) -> None:
        """
        Сохраняет изображение в хранилище.
        :param path: Путь для изображения.
        :param image_stream: Поток с данными изображения.
        """
        ...

    @abstractmethod
    def get_image(self, path: str) -> BytesIO:
        """
        Получает изображение из хранилища.
        :param path: Путь изображения.
        :return: Поток с данными изображения.
        """
        ...

    @abstractmethod
    def delete_image(self, path: str) -> None:
        """
        Удаляет изображение из хранилища.
        :param path: Путь изображения.
        """
        ...
