"""merge heads

Revision ID: 88121ed283e5
Revises: 46b14fd778cd, a1b2c3d4e5f6
Create Date: 2025-12-04 17:27:58.429973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88121ed283e5'
down_revision: Union[str, Sequence[str], None] = ('46b14fd778cd', 'a1b2c3d4e5f6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
