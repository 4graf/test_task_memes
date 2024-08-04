"""
Реализация репозитория S3 хранилища для изображений мемов.
"""
from io import BytesIO

from mypy_boto3_s3.service_resource import Bucket

from app.core.mem.domain.image_repository import ImageRepository
from app.settings import ImageStorageSettings

settings = ImageStorageSettings()


class ImageS3Repository(ImageRepository):
    """
    Реализация репозитория S3 хранилища для изображений мемов.
    """

    def __init__(self, bucket: Bucket):
        """
        Конструктор ImageS3Repository.

        :param client: Клиент для работы с S3 хранилищем.
        """

        # self.client = client
        self.bucket = bucket
        self.bucket_name = settings.bucket_name

    def save_image(self, path: str, image_stream: BytesIO) -> None:
        """
        Сохраняет изображение в хранилище.

        :param path: Путь для изображения.
        :param image_stream: Двоичный поток с данными изображения.
        """
        # self.client.upload_fileobj(Fileobj=image_stream, Bucket=self.bucket_name, Key=path)
        self.bucket.upload_fileobj(Fileobj=image_stream, Key=path)

    def get_image(self, path: str) -> BytesIO:
        """
        Получает изображение из хранилища.
        :param path: Путь для изображения.
        :return: Двоичный поток с данными изображения.
        """
        # self.client.download_fileobj(Bucket=)
        with BytesIO() as image_stream:
            self.bucket.download_fileobj(Key=path, Fileobj=image_stream)
            return image_stream

    def delete_image(self, path: str) -> None:
        """
        Удаляет изображение из хранилища.
        :param path: Путь для изображения.
        """
        ...
