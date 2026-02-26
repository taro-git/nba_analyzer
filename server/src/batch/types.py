from datetime import datetime
from typing import Self


class Season:
    start_year: int
    season_str: str

    def __init__(self, start_year: int, season_str: str) -> None:
        self.start_year = start_year
        self.season_str = season_str

    def minus_one_season(self) -> None:
        self.start_year -= 1
        self.season_str = f"{self.start_year}-{str(self.start_year + 1)[-2:]}"

    @classmethod
    def from_season_str(cls, season_str: str) -> Self:
        start_year = int(season_str[:4])
        return cls(start_year=start_year, season_str=season_str)

    @classmethod
    def from_start_year(cls, start_year: int) -> Self:
        season_str = f"{start_year}-{str(start_year + 1)[-2:]}"
        return cls(start_year=start_year, season_str=season_str)

    @classmethod
    def from_datetime(cls, date: datetime) -> Self:
        start_year = date.year if date.month >= 9 else date.year - 1
        season_str = f"{start_year}-{str(start_year + 1)[-2:]}"
        return cls(start_year=start_year, season_str=season_str)
