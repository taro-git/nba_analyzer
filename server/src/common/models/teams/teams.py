# from sqlalchemy import Enum
from sqlmodel import CheckConstraint, Column, Enum, Field, SQLModel

from common.types import Conference, Division, enum_values


class Team(SQLModel, table=True):
    """
    NBA チームを表すテーブル.
    """

    __tablename__ = "teams"  # type: ignore

    id: int = Field(primary_key=True)
    """チームID"""


class TeamProperty(SQLModel, table=True):
    """
    チーム情報を表すテーブル.
    """

    __tablename__ = "team_properties"  # type: ignore

    season: int = Field(foreign_key="seasons.start_year", primary_key=True)
    """シーズン開始年"""
    team_id: int = Field(foreign_key="teams.id", primary_key=True)
    """チームID"""
    team_city: str = Field(nullable=False)
    """チームの都市名"""
    team_name: str = Field(nullable=False)
    """チーム名"""
    team_tricode: str = Field(nullable=False, max_length=3)
    """チームの三文字コード"""
    conference: Conference = Field(
        sa_column=Column(
            Enum(Conference, values_callable=enum_values),
            nullable=False,
        )
    )
    """チームが所属するカンファレンス"""
    division: Division = Field(
        sa_column=Column(
            Enum(Division, values_callable=enum_values),
            nullable=False,
        )
    )
    """チームが所属するディビジョン"""

    __table_args__ = (
        CheckConstraint(
            "length(team_tricode) = 3",
            name="check_tricode_length",
        ),
        CheckConstraint(
            "(conference = 'East' AND division IN ('Atlantic','Central','SouthEast')) "
            "OR "
            "(conference = 'West' AND division IN ('NorthWest','Pacific','SouthWest','MidWest'))",
            name="check_conference_division_match",
        ),
    )
