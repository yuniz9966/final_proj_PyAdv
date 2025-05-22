from enum import Enum
from django.utils.translation import gettext_lazy as _


class RoomType(str, Enum):
    STUDIO = "Студия"
    ONE_BEDROOM = "Одна спальня"
    TWO_BEDROOM = "Две спальни"
    TWO_BEDROOM_ENSUITE = "Две спальни с отдельными ванными"
    THREE_BEDROOM = "Три спальни"
    ENTIRE_HOUSE = "Дом целиком"
    COTTAGE = "Коттедж"
    PENTHOUSE = "Пентхаус"
    WG_ZIMMER = "Комната в общей квартире (WG)"
    SHARED_ROOM = "Общая комната / койко-место"
    LOFT = "Лофт / Мансарда"
    APARTMENT_WITH_TERRACE = "Квартира с террасой/балконом"

    @classmethod
    def choices(cls):
        return [(member.name, member.value) for member in cls]

    @classmethod
    def faker_choices(cls):
        return [member.value for member in cls]









