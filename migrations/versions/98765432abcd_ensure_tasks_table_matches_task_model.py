"""ensure tasks table matches current Task model

Revision ID: 98765432abcd
Revises: 88121ed283e5
Create Date: 2025-12-05 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98765432abcd'
down_revision = '88121ed283e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    # Inspect existing columns in tasks table to avoid duplicate column errors
    res = conn.execute(sa.text("PRAGMA table_info('tasks')"))
    existing_cols = [r[1] for r in res.fetchall()]

    # Add missing columns if they don't exist
    with op.batch_alter_table('tasks') as batch_op:
        if 'title' not in existing_cols:
            batch_op.add_column(sa.Column('title', sa.String(), nullable=True))
        if 'description' not in existing_cols:
            batch_op.add_column(sa.Column('description', sa.String(), nullable=True))
        if 'owner_id' not in existing_cols:
            batch_op.add_column(sa.Column('owner_id', sa.Integer(), nullable=True))
        if 'date' not in existing_cols:
            batch_op.add_column(sa.Column('date', sa.String(), nullable=True))
        if 'time' not in existing_cols:
            batch_op.add_column(sa.Column('time', sa.String(), nullable=True))
        if 'completed' not in existing_cols:
            batch_op.add_column(sa.Column('completed', sa.Boolean(), nullable=True, server_default='0'))


def downgrade() -> None:
    # This downgrade removes the tasks table columns we added
    # In a real scenario, you might want to preserve the table if it already existed
    conn = op.get_bind()
    res = conn.execute(sa.text("PRAGMA table_info('tasks')"))
    existing_cols = [r[1] for r in res.fetchall()]

    with op.batch_alter_table('tasks') as batch_op:
        # Drop columns if they exist (be careful: this removes data)
        if 'completed' in existing_cols:
            batch_op.drop_column('completed')
        if 'time' in existing_cols:
            batch_op.drop_column('time')
        if 'date' in existing_cols:
            batch_op.drop_column('date')
        if 'owner_id' in existing_cols:
            batch_op.drop_column('owner_id')
        if 'description' in existing_cols:
            batch_op.drop_column('description')
        if 'title' in existing_cols:
            batch_op.drop_column('title')
