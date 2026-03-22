"""empty message

Revision ID: 5b8e32dd6fbc
Revises: a26be94f3425
Create Date: 2026-03-19 19:04:23.323714

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "5b8e32dd6fbc"
down_revision: Union[str, Sequence[str], None] = "a26be94f3425"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.String(), nullable=False),
        sa.Column("season", sa.Integer(), nullable=False),
        sa.Column(
            "category",
            sa.Enum(
                "Preseason",
                "Regular Season",
                "All Star",
                "Playoffs",
                "Play-In Tournament",
                "NBA Cup",
                name="gamecategory",
            ),
            nullable=False,
        ),
        sa.Column("status", sa.Enum("Scheduled", "Live", "Final", name="gamestatus"), nullable=False),
        sa.Column("start_epoc_sec", sa.Integer(), nullable=False),
        sa.Column("elapsed_sec", sa.Integer(), nullable=False),
        sa.Column("home_team_id", sa.Integer(), nullable=False),
        sa.Column("away_team_id", sa.Integer(), nullable=False),
        sa.Column("home_score", sa.Integer(), nullable=False),
        sa.Column("away_score", sa.Integer(), nullable=False),
        sa.Column("playoff_label", sa.String(), nullable=True),
        sa.CheckConstraint("away_score >= 0", name="check_away_score_non_negative"),
        sa.CheckConstraint(
            "(category = 'Playoffs' AND playoff_label IS NOT NULL)"
            " OR (category != 'Playoffs' AND playoff_label IS NULL)",
            name="check_playoffs_has_playoff_label",
        ),
        sa.CheckConstraint("elapsed_sec >= 0", name="check_elapsed_sec_non_negative"),
        sa.CheckConstraint("home_score >= 0", name="check_home_score_non_negative"),
        sa.CheckConstraint("home_team_id != away_team_id", name="check_different_home_team_and_away_team"),
        sa.CheckConstraint("length(game_id) = 10", name="check_game_id_length"),
        sa.CheckConstraint("start_epoc_sec >= 433814400", name="check_start_epoc_sec_larger_than_1983_10_01"),
        sa.ForeignKeyConstraint(
            ["away_team_id"],
            ["teams.id"],
        ),
        sa.ForeignKeyConstraint(
            ["home_team_id"],
            ["teams.id"],
        ),
        sa.ForeignKeyConstraint(
            ["season"],
            ["seasons.start_year"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("game_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("games")
    op.execute("DROP TYPE gamestatus")
    op.execute("DROP TYPE gamecategory")
