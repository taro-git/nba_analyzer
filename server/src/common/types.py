from enum import Enum


def enum_values(enum_cls: type[Enum]) -> list[str]:
    return [e.value for e in enum_cls]


class Conference(Enum):
    """
    NBA チームが所属するカンファレンスを示します.
    """

    west = "West"
    east = "East"

    @classmethod
    def from_str(cls, conference_str: str) -> "Conference":
        """
        カンファレンスを示す文字列から Conference Enum を返します.
        """
        if conference_str.lower().startswith("e"):
            return cls.east
        return cls.west


class Division(Enum):
    """
    NBA チームが所属するディビジョンを示します.
    """

    atlantic = "Atlantic"
    central = "Central"
    southeast = "SouthEast"
    northwest = "NorthWest"
    pacific = "Pacific"
    southwest = "SouthWest"

    @classmethod
    def from_str(cls, division_str: str) -> "Division":
        """
        ディビジョンを示す文字列から Division Enum を返します.
        """
        if division_str.lower().startswith("a"):
            return cls.atlantic
        if division_str.lower().startswith("c"):
            return cls.central
        if division_str.lower().startswith("n"):
            return cls.northwest
        if division_str.lower().startswith("p"):
            return cls.pacific
        if "east" in division_str.lower() or "se" in division_str.lower():
            return cls.southeast
        return cls.southwest
