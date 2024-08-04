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

        :param bucket: Бакет для работы с изображениями в S3 хранилище.
        """

        self.bucket = bucket
        self.bucket_name = settings.bucket_name

    def save_image(self, path: str, image_stream: BytesIO) -> None:
        """
        Сохраняет изображение в хранилище.

        :param path: Путь для изображения.
        :param image_stream: Двоичный поток с данными изображения.
        """
        self.bucket.upload_fileobj(Fileobj=image_stream, Key=path)

    def get_image(self, path: str) -> BytesIO:
        """
        Получает изображение из хранилища.
        :param path: Путь для изображения.
        :return: Двоичный поток с данными изображения.
        """
        image_stream = BytesIO()
        self.bucket.download_fileobj(Key=path, Fileobj=image_stream)
        image_stream.seek(0)
        return image_stream

    def delete_image(self, path: str) -> None:
        """
        Удаляет изображение из хранилища.
        :param path: Путь для изображения.
        """
        self.bucket.delete_objects(Delete={
            'Objects': [
                {
                    'Key': path
                }
            ]
        })
