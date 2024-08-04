from mypy_boto3_s3.service_resource import Bucket

from app.core.shared_kernel.db.dependencies import get_s3_resource
from app.settings import ImageStorageSettings


class CreationHelper:

    @staticmethod
    def create_image_bucket() -> None:

        settings = ImageStorageSettings()

        resource = get_s3_resource()
        image_buckets = [bucket.name == settings.bucket_name for bucket in resource.buckets.all()]
        if len(image_buckets) == 0:
            resource.create_bucket(Bucket=settings.bucket_name)
