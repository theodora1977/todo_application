"""Removed full name and added first and last name

Revision ID: 46b14fd778cd
Revises: 7833cde6dc49
Create Date: 2025-12-01 14:30:26.354932

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '46b14fd778cd'
down_revision: Union[str, Sequence[str], None] = '7833cde6dc49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Make migration idempotent: only add/drop columns if they don't/do exist.
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_cols = {c['name'] for c in inspector.get_columns('users')}

    if 'first_name' not in existing_cols:
        op.add_column('users', sa.Column('first_name', sa.String(), nullable=True))

    if 'last_name' not in existing_cols:
        op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))

    if 'full_name' in existing_cols:
        op.drop_column('users', 'full_name')

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # Make downgrade idempotent as well
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_cols = {c['name'] for c in inspector.get_columns('users')}

    if 'full_name' not in existing_cols:
        op.add_column('users', sa.Column('full_name', sa.VARCHAR(), nullable=False))

    if 'last_name' in existing_cols:
        op.drop_column('users', 'last_name')

    if 'first_name' in existing_cols:
        op.drop_column('users', 'first_name')

    # ### end Alembic commands ###
