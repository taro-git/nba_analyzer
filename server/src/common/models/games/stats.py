from sqlmodel import CheckConstraint, Field, SQLModel, UniqueConstraint


class Stats(SQLModel, table=True):
    """
    スタッツ.
    """

    __tablename__ = "stats"  # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    """内部管理のためのID"""
    game_id: int | None = Field(nullable=True, foreign_key="games.id", default=None)
    """試合の内部管理用ID"""
    game_player_id: int | None = Field(nullable=True, foreign_key="game_players.id", default=None)
    """試合に紐づいている選手の内部管理用ID"""
    team_id: int | None = Field(nullable=True, foreign_key="teams.id", default=None)
    """チームID"""
    elapsed_ms: int = Field(nullable=False)
    """試合の経過時間(ミリ秒)"""
    ms: int = Field(nullable=False)
    """出場時間(ミリ秒)"""
    points: int = Field(nullable=False)
    """得点"""
    offence_rebounds: int = Field(nullable=False)
    """オフェンスバウンド"""
    diffence_rebounds: int = Field(nullable=False)
    """ディフェンスバウンド"""
    assists: int = Field(nullable=False)
    """アシスト"""
    steals: int = Field(nullable=False)
    """スティール"""
    blocks: int = Field(nullable=False)
    """ブロック"""
    field_goal_attempts: int = Field(nullable=False)
    """フィールドゴール試行回数"""
    field_goal_made: int = Field(nullable=False)
    """フィールドゴール成功数"""
    three_point_attempts: int = Field(nullable=False)
    """三ポイント試行回数"""
    three_point_made: int = Field(nullable=False)
    """三ポイント成功数"""
    free_throw_attempts: int = Field(nullable=False)
    """フリースロー試行回数"""
    free_throw_made: int = Field(nullable=False)
    """フリースロー成功数"""
    turnovers: int = Field(nullable=False)
    """ターンオーバー"""
    blocked_shots_received: int | None = Field(nullable=True, default=None)
    """被ブロック数"""
    personal_fouls: int = Field(nullable=False)
    """パーソナルファール"""
    technical_fouls: int | None = Field(nullable=True, default=None)
    """テクニカルファール"""
    fouls_drawn: int | None = Field(nullable=True, default=None)
    """被ファール数"""
    plus: int | None = Field(nullable=True, default=None)
    """出場中のチーム全体の得点"""
    plus_minus: int = Field(nullable=False)
    """出場中のチーム全体の得失点差"""

    __table_args__ = (
        UniqueConstraint(
            "game_id",
            "game_player_id",
            "elapsed_ms",
            name="unique_game_id_and_game_player_id_and_elapsed_ms_constraint",
        ),
        UniqueConstraint(
            "game_id",
            "team_id",
            "elapsed_ms",
            name="unique_game_id_and_team_id_and_elapsed_ms_constraint",
        ),
        CheckConstraint(
            "(game_player_id IS NOT NULL AND team_id IS NULL)OR (game_player_id IS NULL OR team_id IS NOT NULL)",
            name="check_game_player_id_and_team_id_constraint",
        ),
        CheckConstraint(
            "elapsed_ms >= 0",
            name="check_elapsed_ms_non_negative",
        ),
        CheckConstraint(
            "ms >= 0",
            name="check_sec_non_negative",
        ),
        CheckConstraint(
            "points >= 0",
            name="check_points_non_negative",
        ),
        CheckConstraint(
            "offence_rebounds >= 0",
            name="check_offence_rebounds_non_negative",
        ),
        CheckConstraint(
            "diffence_rebounds >= 0",
            name="check_diffence_rebounds_non_negative",
        ),
        CheckConstraint(
            "assists >= 0",
            name="check_assists_non_negative",
        ),
        CheckConstraint(
            "steals >= 0",
            name="check_steals_non_negative",
        ),
        CheckConstraint(
            "blocks >= 0",
            name="check_blocks_non_negative",
        ),
        CheckConstraint(
            "field_goal_attempts >= 0",
            name="check_field_goal_attempts_non_negative",
        ),
        CheckConstraint(
            "field_goal_made >= 0",
            name="check_field_goal_made_non_negative",
        ),
        CheckConstraint(
            "three_point_attempts >= 0",
            name="check_three_point_attempts_non_negative",
        ),
        CheckConstraint(
            "three_point_made >= 0",
            name="check_three_point_made_non_negative",
        ),
        CheckConstraint(
            "free_throw_attempts >= 0",
            name="check_free_throw_attempts_non_negative",
        ),
        CheckConstraint(
            "free_throw_made >= 0",
            name="check_free_throw_made_non_negative",
        ),
        CheckConstraint(
            "turnovers >= 0",
            name="check_turnovers_non_negative",
        ),
        CheckConstraint(
            "blocked_shots_received IS NULL OR blocked_shots_received >= 0",
            name="check_blocked_shots_received_non_negative",
        ),
        CheckConstraint(
            "personal_fouls >= 0",
            name="check_personal_fouls_non_negative",
        ),
        CheckConstraint(
            "technical_fouls IS NULL OR technical_fouls >= 0",
            name="check_technical_fouls_non_negative",
        ),
        CheckConstraint(
            "fouls_drawn IS NULL OR fouls_drawn >= 0",
            name="check_fouls_drawn_non_negative",
        ),
        CheckConstraint(
            "plus IS NULL OR plus >= 0",
            name="check_plus_non_negative",
        ),
        CheckConstraint(
            "field_goal_made <= field_goal_attempts "
            "AND three_point_made <= three_point_attempts "
            "AND free_throw_made <= free_throw_attempts ",
            name="check_attempts_greater_than_made",
        ),
    )
