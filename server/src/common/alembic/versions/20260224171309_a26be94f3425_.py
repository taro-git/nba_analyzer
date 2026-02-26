"""empty message

Revision ID: a26be94f3425
Revises: 7ecb1c5e0e6b
Create Date: 2026-02-24 17:13:09.791861

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a26be94f3425"
down_revision: Union[str, Sequence[str], None] = "7ecb1c5e0e6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "caches",
        sa.Column("request_hash", sa.BigInteger(), nullable=False),
        sa.Column("response", sa.JSON(), nullable=False),
        sa.Column("expires_at", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("request_hash"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("caches")
