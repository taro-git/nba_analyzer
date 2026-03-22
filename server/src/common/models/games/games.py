from sqlmodel import CheckConstraint, Column, Enum, Field, SQLModel

from common.types import GameCategory, GameStatus, enum_values


class Game(SQLModel, table=True):
    """
    試合を表すテーブル.
    """

    __tablename__ = "games"  # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    """内部管理のためのID"""
    game_id: str = Field(nullable=False, max_length=10, unique=True)
    """試合ID"""
    season: int = Field(foreign_key="seasons.start_year")
    """シーズン開始年"""
    category: GameCategory = Field(
        sa_column=Column(
            Enum(GameCategory, values_callable=enum_values),
            nullable=False,
        )
    )
    """試合カテゴリ"""
    status: GameStatus = Field(
        sa_column=Column(
            Enum(GameStatus, values_callable=enum_values),
            nullable=False,
        )
    )
    """試合ステータス"""
    start_epoc_sec: int = Field(nullable=False)
    """試合開始時刻"""
    elapsed_sec: int = Field(nullable=False)
    """試合経過時間"""
    home_team_id: int = Field(foreign_key="teams.id")
    """ホームチームのチームID"""
    away_team_id: int = Field(foreign_key="teams.id")
    """アウェイチームのチームID"""
    home_score: int = Field(nullable=False)
    """ホームチームのスコア"""
    away_score: int = Field(nullable=False)
    """アウェイチームのスコア"""
    playoff_label: str | None = Field(nullable=True)
    """プレーオフの詳細を表すラベル"""

    __table_args__ = (
        CheckConstraint(
            "length(game_id) = 10",
            name="check_game_id_length",
        ),
        CheckConstraint(
            "home_team_id != away_team_id",
            name="check_different_home_team_and_away_team",
        ),
        CheckConstraint(
            "home_score >= 0",
            name="check_home_score_non_negative",
        ),
        CheckConstraint(
            "away_score >= 0",
            name="check_away_score_non_negative",
        ),
        CheckConstraint(
            "elapsed_sec >= 0",
            name="check_elapsed_sec_non_negative",
        ),
        CheckConstraint(
            "start_epoc_sec >= 433814400",
            name="check_start_epoc_sec_larger_than_1983_10_01",
        ),
        CheckConstraint(
            "(category = 'Playoffs' AND playoff_label IS NOT NULL)"
            " OR (category != 'Playoffs' AND playoff_label IS NULL)",
            name="check_playoffs_has_playoff_label",
        ),
    )
