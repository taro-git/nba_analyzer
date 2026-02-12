import re
from enum import Enum
from typing import List, Self, Type

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, GetCoreSchemaHandler, model_validator
from pydantic.alias_generators import to_camel
from pydantic_core import core_schema
from sqlmodel import Field, Session

from common.db import get_session

# ======================================================================================================================
# Schemas
# ======================================================================================================================


class Season(str):
    """
    パラメータや戻り値に使用するシーズンの型を示します.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: Type[object],
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, season: str) -> str:
        match = re.fullmatch(r"(\d{4})-(\d{2})", season)
        if not match:
            raise ValueError("season must be YYYY-YY format and >= 1970-71")

        year_str, suffix = match.groups()
        year = int(year_str)
        expected_suffix = f"{(year + 1) % 100:02d}"

        if year < 1970 or suffix != expected_suffix:
            raise ValueError("season must be YYYY-YY format and >= 1970-71")
        return season


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


class TeamStanding(BaseModel):
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

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class RegularSeasonStandingsSchema(BaseModel):
    """
    全チームのレギュラーシーズンの成績を示します.
    """

    season: Season
    """シーズン開始年"""
    teams: List[TeamStanding]
    """チーム成績一覧"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


# ======================================================================================================================
# Routes
# ======================================================================================================================
regular_season_standings_router = APIRouter()


@regular_season_standings_router.get("/standings/regular-seasons/{season}")
async def list_regular_season_standings_by_season(
    season: Season, session: Session = Depends(get_session)
) -> RegularSeasonStandingsSchema:
    """
    シーズンを指定してレギュラーシーズンのチーム成績一覧を返します.
    """
    print(session)
    dummy_team = TeamStanding(
        team_id=0,
        team_name="dummy_team_name",
        team_tricode="CRE",
        team_logo="https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        conference=Conference.east,
        division=Division.southeast,
        rank=1,
        win=1,
        lose=1,
    )
    dummy_team_2 = TeamStanding(
        team_id=0,
        team_name="dummy_team_name",
        team_tricode="IND",
        team_logo="https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        conference=Conference.east,
        division=Division.southeast,
        rank=2,
        win=0,
        lose=1,
    )
    dummy_team_3 = TeamStanding(
        team_id=0,
        team_name="dummy_team_name",
        team_tricode="GSW",
        team_logo="https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        conference=Conference.west,
        division=Division.southwest,
        rank=2,
        win=1,
        lose=1,
    )
    dummy_team_4 = TeamStanding(
        team_id=0,
        team_name="dummy_team_name",
        team_tricode="LAC",
        team_logo="https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        conference=Conference.west,
        division=Division.southwest,
        rank=1,
        win=1,
        lose=0,
    )
    return RegularSeasonStandingsSchema(season=season, teams=[dummy_team, dummy_team_2, dummy_team_3, dummy_team_4])
