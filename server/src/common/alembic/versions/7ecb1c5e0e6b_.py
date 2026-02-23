# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
"""empty message

Revision ID: 7ecb1c5e0e6b
Revises:
Create Date: 2026-02-14 00:58:10.432450

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import String

revision: str = "7ecb1c5e0e6b"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "seasons",
        sa.Column("start_year", sa.Integer(), nullable=False),
        sa.CheckConstraint("start_year >= 1970", name="check_start_year_gt_1970"),
        sa.PrimaryKeyConstraint("start_year"),
    )
    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_city", String(), nullable=False),
        sa.Column("team_name", String(), nullable=False),
        sa.Column("team_tricode", String(length=3), nullable=False),
        sa.Column("conference", sa.Enum("West", "East", name="conference"), nullable=False),
        sa.Column(
            "division",
            sa.Enum("Atlantic", "Central", "SouthEast", "NorthWest", "Pacific", "SouthWest", name="division"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "(conference = 'East' AND division IN ('Atlantic','Central','SouthEast'))"
            " OR (conference = 'West' AND division IN ('NorthWest','Pacific','SouthWest'))",
            name="check_conference_division_match",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "regular_season_team_standings",
        sa.Column("season", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("win", sa.Integer(), nullable=False),
        sa.Column("lose", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["season"], ["seasons.start_year"]),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.PrimaryKeyConstraint("season", "team_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("regular_season_team_standings")
    op.drop_table("teams")
    op.drop_table("seasons")
    op.execute("DROP TYPE conference")
    op.execute("DROP TYPE division")
