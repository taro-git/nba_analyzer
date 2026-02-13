from typing import List, Self

from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.alias_generators import to_camel
from sqlmodel import Field

from common.types import Conference, Division
from rest_api.schemas.commons import Season


class RegularSeasonTeam(BaseModel):
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


class RegularSeasonTeamsSchema(BaseModel):
    """
    全チームのレギュラーシーズンの成績を示します.
    """

    season: Season
    """シーズン開始年"""
    teams: List[RegularSeasonTeam]
    """チーム成績一覧"""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )
