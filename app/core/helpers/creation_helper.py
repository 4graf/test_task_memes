"""
Класс-помощник для инициализации системы.
Включает в себя: создание бакета изображений в S3, создание базового (первого) администратора.
"""
from app.api.users.dependencies import get_user_service
from app.core.shared_kernel.db.dependencies import get_s3_resource, get_async_db_session, async_session_maker
from app.core.shared_kernel.domain.value_objects.user_role import UserRole
from app.core.user.application.user.schemas.name_info_schema import NameInfoSchema
from app.core.user.application.user.schemas.user_create_schema import UserCreateSchema
from app.core.user.domain.value_object.user_name import UserName
from app.settings import ImageStorageSettings, BaseAdminSettings


class CreationHelper:
    """
    Класс-помощник для инициализации системы.
    """
    @staticmethod
    def create_image_bucket() -> None:
        """
        Создание бакета изображений в S3, если его ещё нет.
        """
        settings = ImageStorageSettings()

        resource = get_s3_resource()
        image_buckets = [bucket.name == settings.bucket_name for bucket in resource.buckets.all()]
        if len(image_buckets) == 0:
            resource.create_bucket(Bucket=settings.bucket_name)

    @staticmethod
    async def create_base_admin() -> None:
        """
        Создание базового пользователя-администратора, если администраторов ещё нет.
        """
        settings = BaseAdminSettings()

        async with async_session_maker() as session:
            user_service = await get_user_service(session)
            admins = await user_service.get_users_by_role(role=UserRole.ADMIN)

            if len(admins) == 0:
                admin = UserCreateSchema(
                    login=settings.login.get_secret_value(),
                    password=settings.password.get_secret_value(),
                    email=settings.email.get_secret_value(),
                    name=NameInfoSchema(first_name=settings.first_name,
                                        second_name=settings.second_name),
                    role=UserRole.ADMIN
                )

                await user_service.create_user(admin)
