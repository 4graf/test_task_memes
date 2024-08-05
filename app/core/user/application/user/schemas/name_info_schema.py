from pydantic import BaseModel

from app.core.user.domain.value_object.user_name import UserName


class NameInfoSchema(BaseModel):
    first_name: str
    second_name: str | None

    @classmethod
    def from_entity_vo(cls, user_name: UserName) -> "NameInfoSchema":
        return cls(
            first_name=user_name.first_name,
            second_name=user_name.second_name
        )
