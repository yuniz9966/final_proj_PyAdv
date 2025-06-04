from enum import Enum


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
        return [member.name for member in cls]

    @classmethod
    def get_varname_by_value(cls, value):
        for member in cls:
            if member.value == value:
                return member.name












