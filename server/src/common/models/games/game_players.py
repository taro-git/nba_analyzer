from sqlmodel import CheckConstraint, Column, Enum, Field, SQLModel, UniqueConstraint

from common.types import PlayerPosition, enum_values


class GamePlayer(SQLModel, table=True):
    """
    試合に紐づいている選手.
    """

    __tablename__ = "game_players"  # type: ignore

    id: int | None = Field(primary_key=True, default=None)
    """内部管理のためのID"""
    game_id: int = Field(nullable=False, foreign_key="games.id")
    """試合の内部管理用ID"""
    player_id: int = Field(nullable=False, foreign_key="players.id")
    """選手ID"""
    jearsy_num: str = Field(nullable=False)
    """背番号"""
    position: PlayerPosition | None = Field(
        sa_column=Column(
            Enum(PlayerPosition, values_callable=enum_values),
            nullable=True,
        ),
        default=None,
    )
    """ポジション"""
    is_home: bool = Field(nullable=False)
    """ホームチームか否か"""
    is_starter: bool = Field(nullable=False)
    """スターティングメンバーか否か"""
    is_active: bool = Field(nullable=False)
    """アクティブか否か"""

    __table_args__ = (
        UniqueConstraint(
            "game_id",
            "player_id",
            name="unique_game_id_and_player_id_constraint",
        ),
        CheckConstraint(
            "(is_starter AND is_active) OR NOT is_starter",
            name="check_starter_is_active",
        ),
    )
