from enum import Enum


class Conference(Enum):
    """
    NBA チームが所属するカンファレンスを示します.
    """

    west = "West"
    east = "East"


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
