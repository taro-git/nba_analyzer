from datetime import date

from sqlmodel import Column, Enum, Field, SQLModel

from common.types import PlayerPosition, enum_values


class Player(SQLModel, table=True):
    """
    選手の共通情報.
    """

    __tablename__ = "players"  # type: ignore

    id: int = Field(primary_key=True)
    """選手ID"""
    updated_at: int = Field(nullable=False)
    """更新日時(エポック秒)"""
    full_name: str = Field(nullable=False)
    """フルネーム"""
    abbreviation: str = Field(nullable=False)
    """略名"""
    date_of_birth: date | None = Field(nullable=True, default=None)
    """生年月日"""
    draft_year: int | None = Field(nullable=True, default=None)
    """ドラフト年"""
    position: PlayerPosition | None = Field(
        sa_column=Column(
            Enum(PlayerPosition, values_callable=enum_values),
            nullable=True,
        ),
        default=None,
    )
    """ポジション"""
    team_id: int | None = Field(nullable=True, foreign_key="teams.id", default=None)
    """所属チーム"""
