from pydantic import BaseModel, EmailStr

from app.core.user.application.user.schemas.name_info_schema import NameInfoSchema
from app.core.shared_kernel.domain.value_objects.user_role import UserRole


class UserRegisterSchema(BaseModel):
    login: str
    password: str
    email: EmailStr
    name: NameInfoSchema
