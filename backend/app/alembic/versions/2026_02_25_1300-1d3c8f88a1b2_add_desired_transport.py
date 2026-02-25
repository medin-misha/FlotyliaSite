"""add desired_transport

Revision ID: 1d3c8f88a1b2
Revises: 8a49cbcff8c5
Create Date: 2026-02-25 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1d3c8f88a1b2"
down_revision: Union[str, Sequence[str], None] = "8a49cbcff8c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user", sa.Column("desired_transport", sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user", "desired_transport")
