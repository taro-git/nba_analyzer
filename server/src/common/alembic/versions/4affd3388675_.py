"""empty message

Revision ID: 4affd3388675
Revises: 7ecb1c5e0e6b
Create Date: 2026-02-21 17:37:20.610644

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "4affd3388675"
down_revision: Union[str, Sequence[str], None] = "7ecb1c5e0e6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "caches",
        sa.Column("request_hash", sa.BigInteger(), nullable=False),
        sa.Column("response", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("expires_at", postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("request_hash"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("caches")
