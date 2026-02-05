from enum import Enum
from typing import List, Self

from fastapi import APIRouter, Depends
from pydantic import field_validator, model_validator
from sqlmodel import Field, Session, SQLModel

from common.db import get_session


# ======================================================================================================================
# Schemas
# ======================================================================================================================
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


class TeamStanding(SQLModel):
    """
    1チームのレギュラーシーズンの成績を示します.
    """

    team_id: int
    """チームID"""
    team_name: str
    """チーム名"""
    team_tricode: str = Field(min_length=3, max_length=3)
    """3桁のチーム略称"""
    team_logo: str  # f"https://cdn.nba.com/logos/nba/{team_id}/global/L/logo.svg"
    """チームロゴ取得先 URL"""
    conference: Conference
    """カンファレンス"""
    division: Division
    """ディビジョン"""
    rank: int
    """シーズン順位"""
    win: int
    """シーズン勝利数"""
    lose: int
    """シーズン敗北数"""

    @model_validator(mode="after")
    def validate_combination_between_conference_and_division(self) -> Self:
        if (
            (
                self.conference == Conference.east
                and (
                    self.division == Division.northwest
                    or self.division == Division.pacific
                    or self.division == Division.southwest
                )
            )
            or self.conference == Conference.west
            and (
                self.division == Division.atlantic
                or self.division == Division.central
                or self.division == Division.southeast
            )
        ):
            raise ValueError(f"division: {self.division} is not in conference: {self.conference}")
        return self


class RegularSeasonStandingsSchema(SQLModel):
    """
    全チームのレギュラーシーズンの成績を示します.
    """

    season: int
    """シーズン開始年"""
    teams: List[TeamStanding]
    """チーム成績一覧"""

    @field_validator("season")
    @classmethod
    def validate_season(cls, season: int) -> int:
        if season < 1946:
            raise ValueError("season must be >= 1946")
        return season


# ======================================================================================================================
# Routes
# ======================================================================================================================
regular_season_standings_router = APIRouter()


@regular_season_standings_router.get("/standings/regular-seasons/{season}")
async def list_regular_season_standings_by_season(
    season: int, session: Session = Depends(get_session)
) -> RegularSeasonStandingsSchema:
    """
    シーズンを指定してレギュラーシーズンのチーム成績一覧を返します.
    """
    print(session)
    dummy_team = TeamStanding(
        team_id=0,
        team_name="dummy_team_name",
        team_tricode="DTN",
        team_logo="https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        conference=Conference.west,
        division=Division.southwest,
        rank=1,
        win=1,
        lose=1,
    )
    return RegularSeasonStandingsSchema(season=season, teams=[dummy_team])
