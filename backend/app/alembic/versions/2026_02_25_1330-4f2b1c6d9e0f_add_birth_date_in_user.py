"""add birth_date in user

Revision ID: 4f2b1c6d9e0f
Revises: 1d3c8f88a1b2
Create Date: 2026-02-25 13:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4f2b1c6d9e0f"
down_revision: Union[str, Sequence[str], None] = "1d3c8f88a1b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user", sa.Column("birth_date", sa.Date(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user", "birth_date")
