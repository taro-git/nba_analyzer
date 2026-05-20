from sqlmodel import CheckConstraint, Field, SQLModel, UniqueConstraint


class GameAction(SQLModel, table=True):
    """
    試合の1プレー.
    """

    __tablename__ = "game_actions"  # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    """内部管理のためのID"""
    game_id: int = Field(nullable=False, foreign_key="games.id")
    """試合の内部管理用ID"""
    action_number: int = Field(nullable=False)
    """アクション番号"""
    elapsed_ms: int = Field(nullable=False)
    """試合の経過時間(ミリ秒)"""
    game_player_id: int | None = Field(nullable=True, foreign_key="game_players.id", default=None)
    """試合に紐づいている選手の内部管理用ID"""
    team_id: int | None = Field(nullable=True, foreign_key="teams.id", default=None)
    """チームID"""
    description: str = Field(nullable=False)
    """アクションの詳細"""
    action_type: str = Field(nullable=False)
    """アクションの種類"""
    sub_type: str | None = Field(nullable=True, default=None)
    """アクションのサブタイプ"""
    shot_value: int | None = Field(nullable=True, default=None)
    """ショットの得点数"""
    home_score: int | None = Field(nullable=True, default=None)
    """ホームチームの得点数"""
    away_score: int | None = Field(nullable=True, default=None)
    """アウェイチームの得点数"""
    x_legacy: int | None = Field(nullable=True, default=None)
    """X 座標"""
    y_legacy: int | None = Field(nullable=True, default=None)
    """Y 座標"""

    __table_args__ = (
        UniqueConstraint(
            "game_id",
            "action_number",
            name="unique_game_id_and_action_number_constraint",
        ),
        CheckConstraint(
            "elapsed_ms >= 0",
            name="check_elapsed_ms_non_negative",
        ),
        CheckConstraint(
            "shot_value IS NULL OR shot_value = 1 OR shot_value = 2 OR shot_value = 3",
            name="check_shot_value_valid",
        ),
        CheckConstraint(
            "home_score IS NULL OR home_score >= 0",
            name="check_home_score_non_negative",
        ),
        CheckConstraint(
            "away_score IS NULL OR away_score >= 0",
            name="check_away_score_non_negative",
        ),
    )
