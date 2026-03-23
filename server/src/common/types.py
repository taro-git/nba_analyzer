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
        if conference_str.lower().startswith("w"):
            return cls.west
        raise ValueError(f"Invalid conference_str: {conference_str}")


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
    midwest = "MidWest"

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
        if division_str.lower().startswith("s"):
            if "east" in division_str.lower() or "se" in division_str.lower():
                return cls.southeast
            if "west" in division_str.lower() or "sw" in division_str.lower():
                return cls.southwest
        if division_str.lower().startswith("m"):
            return cls.midwest
        raise ValueError(f"Invalid division_str: {division_str}")


class GameCategory(Enum):
    preseason = "Preseason"
    regular_season = "Regular Season"
    all_star = "All Star"
    playoffs = "Playoffs"
    playin_tournament = "Play-In Tournament"
    nba_cup = "NBA Cup"

    @classmethod
    def from_game_id(cls, game_id: str) -> "GameCategory":
        try:
            if game_id[2] == "1" or game_id[2] == "9":
                return cls.preseason
            if game_id[2] == "2":
                return cls.regular_season
            if game_id[2] == "3":
                return cls.all_star
            if game_id[2] == "4":
                return cls.playoffs
            if game_id[2] == "5":
                return cls.playin_tournament
            if game_id[2] == "6":
                return cls.nba_cup
        except Exception:
            pass
        raise ValueError(f"Invalid game_id: {game_id}")


class GameStatus(Enum):
    scheduled = "Scheduled"
    live = "Live"
    final = "Final"

    @classmethod
    def from_status_id(cls, status_id: int) -> "GameStatus":
        if status_id == 1:
            return cls.scheduled
        if status_id == 2:
            return cls.live
        if status_id == 3:
            return cls.final
        raise ValueError(f"Invalid status_id: {status_id}")
