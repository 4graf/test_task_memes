from pydantic import BaseModel, EmailStr

from app.core.shared_kernel.domain.value_objects.user_role import UserRole
from app.core.user.application.user.schemas.name_info_schema import NameInfoSchema


class UserCreateSchema(BaseModel):
    login: str
    password: str
    email: EmailStr
    name: NameInfoSchema
    role: UserRole
