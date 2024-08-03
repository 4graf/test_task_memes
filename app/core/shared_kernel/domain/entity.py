from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class BaseEntity:
    """
    Базовый класс для всех сущностей

    :cvar uuid: Уникальный идентификатор сущности.
    """

    uuid: Any

    def __eq__(self, other: Any) -> bool:
        """
        Проверяет эквивалентность сущности по id.

        :param other: Вторая сущность.
        :return: True, если сущности эквивалентны, False, если сущности неэквивалентны.
        """
        if isinstance(other, self.__class__):
            return self.uuid == other.uuid
        return False
