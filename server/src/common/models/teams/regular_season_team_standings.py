from sqlmodel import Field, SQLModel


class RegularSeasonTeamStanding(SQLModel, table=True):
    """
    レギュラーシーズンのチーム順位を表すテーブル.
    """

    __tablename__ = "regular_season_team_standings"  # type: ignore

    season: int = Field(foreign_key="seasons.start_year", primary_key=True)
    """シーズン開始年"""
    team_id: int = Field(foreign_key="teams.id", primary_key=True)
    """チームID"""
    rank: int = Field(nullable=False)
    """順位"""
    win: int = Field(nullable=False)
    """勝利数"""
    lose: int = Field(nullable=False)
    """敗戦数"""
