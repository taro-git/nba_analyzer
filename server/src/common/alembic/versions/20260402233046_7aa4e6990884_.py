"""empty message

Revision ID: 7aa4e6990884
Revises: 5b8e32dd6fbc
Create Date: 2026-04-02 23:30:46.789116

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "7aa4e6990884"
down_revision: Union[str, Sequence[str], None] = "5b8e32dd6fbc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("abbreviation", sa.String(), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("draft_year", sa.Integer(), nullable=True),
        sa.Column("position", sa.Enum("PG", "SG", "SF", "PF", "C", name="playerposition"), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "game_players",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("jearsy_num", sa.String(), nullable=False),
        sa.Column("position", sa.Enum("PG", "SG", "SF", "PF", "C", name="playerposition"), nullable=True),
        sa.Column("is_home", sa.Boolean(), nullable=False),
        sa.Column("is_starter", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.CheckConstraint("(is_starter AND is_active) OR NOT is_starter", name="check_starter_is_active"),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.id"],
        ),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["players.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("game_id", "player_id", name="unique_game_id_and_player_id_constraint"),
    )
    op.create_table(
        "game_actions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("action_number", sa.Integer(), nullable=False),
        sa.Column("elapsed_ms", sa.Integer(), nullable=False),
        sa.Column("game_player_id", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("action_type", sa.String(), nullable=False),
        sa.Column("sub_type", sa.String(), nullable=True),
        sa.Column("shot_value", sa.Integer(), nullable=True),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
        sa.Column("x_legacy", sa.Integer(), nullable=True),
        sa.Column("y_legacy", sa.Integer(), nullable=True),
        sa.CheckConstraint("away_score IS NULL OR away_score >= 0", name="check_away_score_non_negative"),
        sa.CheckConstraint("elapsed_ms >= 0", name="check_elapsed_ms_non_negative"),
        sa.CheckConstraint("home_score IS NULL OR home_score >= 0", name="check_home_score_non_negative"),
        sa.CheckConstraint(
            "shot_value IS NULL OR shot_value = 1 OR shot_value = 2 OR shot_value = 3", name="check_shot_value_valid"
        ),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.id"],
        ),
        sa.ForeignKeyConstraint(
            ["game_player_id"],
            ["game_players.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("game_id", "action_number", name="unique_game_id_and_action_number_constraint"),
    )
    op.create_table(
        "stats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=True),
        sa.Column("game_player_id", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("elapsed_ms", sa.Integer(), nullable=False),
        sa.Column("ms", sa.Integer(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("offence_rebounds", sa.Integer(), nullable=False),
        sa.Column("diffence_rebounds", sa.Integer(), nullable=False),
        sa.Column("assists", sa.Integer(), nullable=False),
        sa.Column("steals", sa.Integer(), nullable=False),
        sa.Column("blocks", sa.Integer(), nullable=False),
        sa.Column("field_goal_attempts", sa.Integer(), nullable=False),
        sa.Column("field_goal_made", sa.Integer(), nullable=False),
        sa.Column("three_point_attempts", sa.Integer(), nullable=False),
        sa.Column("three_point_made", sa.Integer(), nullable=False),
        sa.Column("free_throw_attempts", sa.Integer(), nullable=False),
        sa.Column("free_throw_made", sa.Integer(), nullable=False),
        sa.Column("turnovers", sa.Integer(), nullable=False),
        sa.Column("blocked_shots_received", sa.Integer(), nullable=True),
        sa.Column("personal_fouls", sa.Integer(), nullable=False),
        sa.Column("technical_fouls", sa.Integer(), nullable=True),
        sa.Column("fouls_drawn", sa.Integer(), nullable=True),
        sa.Column("plus", sa.Integer(), nullable=True),
        sa.Column("plus_minus", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "(game_player_id IS NOT NULL AND team_id IS NULL) OR (game_player_id IS NULL OR team_id IS NOT NULL)",
            name="check_game_player_id_and_team_id_constraint",
        ),
        sa.CheckConstraint("assists >= 0", name="check_assists_non_negative"),
        sa.CheckConstraint(
            "blocked_shots_received IS NULL OR blocked_shots_received >= 0",
            name="check_blocked_shots_received_non_negative",
        ),
        sa.CheckConstraint("blocks >= 0", name="check_blocks_non_negative"),
        sa.CheckConstraint("diffence_rebounds >= 0", name="check_diffence_rebounds_non_negative"),
        sa.CheckConstraint("elapsed_ms >= 0", name="check_elapsed_ms_non_negative"),
        sa.CheckConstraint("field_goal_attempts >= 0", name="check_field_goal_attempts_non_negative"),
        sa.CheckConstraint(
            "field_goal_made <= field_goal_attempts"
            " AND three_point_made <= three_point_attempts"
            " AND free_throw_made <= free_throw_attempts ",
            name="check_attempts_greater_than_made",
        ),
        sa.CheckConstraint("field_goal_made >= 0", name="check_field_goal_made_non_negative"),
        sa.CheckConstraint("fouls_drawn IS NULL OR fouls_drawn >= 0", name="check_fouls_drawn_non_negative"),
        sa.CheckConstraint("free_throw_attempts >= 0", name="check_free_throw_attempts_non_negative"),
        sa.CheckConstraint("free_throw_made >= 0", name="check_free_throw_made_non_negative"),
        sa.CheckConstraint("offence_rebounds >= 0", name="check_offence_rebounds_non_negative"),
        sa.CheckConstraint("personal_fouls >= 0", name="check_personal_fouls_non_negative"),
        sa.CheckConstraint("plus IS NULL OR plus >= 0", name="check_plus_non_negative"),
        sa.CheckConstraint("points >= 0", name="check_points_non_negative"),
        sa.CheckConstraint("ms >= 0", name="check_ms_non_negative"),
        sa.CheckConstraint("steals >= 0", name="check_steals_non_negative"),
        sa.CheckConstraint(
            "technical_fouls IS NULL OR technical_fouls >= 0", name="check_technical_fouls_non_negative"
        ),
        sa.CheckConstraint("three_point_attempts >= 0", name="check_three_point_attempts_non_negative"),
        sa.CheckConstraint("three_point_made >= 0", name="check_three_point_made_non_negative"),
        sa.CheckConstraint("turnovers >= 0", name="check_turnovers_non_negative"),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.id"],
        ),
        sa.ForeignKeyConstraint(
            ["game_player_id"],
            ["game_players.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["teams.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "game_id",
            "game_player_id",
            "elapsed_ms",
            name="unique_game_id_and_game_player_id_and_elapsed_ms_constraint",
        ),
        sa.UniqueConstraint(
            "game_id", "team_id", "elapsed_ms", name="unique_game_id_and_team_id_and_elapsed_ms_constraint"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("stats")
    op.drop_table("game_actions")
    op.drop_table("game_players")
    op.drop_table("players")
    op.execute("DROP TYPE playerposition")
