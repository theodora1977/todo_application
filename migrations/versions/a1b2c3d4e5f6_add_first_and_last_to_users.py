"""add first_name and last_name to users, migrate full_name -> first/last

Revision ID: a1b2c3d4e5f6
Revises: 7833cde6dc49
Create Date: 2025-12-04 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '7833cde6dc49'
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    # Inspect existing columns to avoid duplicate column errors
    res = conn.execute(sa.text("PRAGMA table_info('users')"))
    existing_cols = [r[1] for r in res.fetchall()]

    # Add new nullable columns only if they don't already exist
    if 'first_name' not in existing_cols or 'last_name' not in existing_cols:
        with op.batch_alter_table('users') as batch_op:
            if 'first_name' not in existing_cols:
                batch_op.add_column(sa.Column('first_name', sa.String(), nullable=True))
            if 'last_name' not in existing_cols:
                batch_op.add_column(sa.Column('last_name', sa.String(), nullable=True))

    # Migrate data from full_name into first_name and last_name (SQLite compatible)
    # Only run if full_name exists
    if 'full_name' in existing_cols:
        # Split on first space: first part -> first_name, remainder -> last_name
        op.execute(sa.text(
            """
            UPDATE users
            SET
                first_name = CASE
                    WHEN instr(full_name, ' ') > 0 THEN substr(full_name, 1, instr(full_name, ' ') - 1)
                    ELSE full_name
                END,
                last_name = CASE
                    WHEN instr(full_name, ' ') > 0 THEN substr(full_name, instr(full_name, ' ') + 1)
                    ELSE ''
                END
            WHERE full_name IS NOT NULL;
            """
        ))

        # Now drop the old column
        # Recompute existing_cols because the table structure may have changed
        res = conn.execute(sa.text("PRAGMA table_info('users')"))
        existing_cols = [r[1] for r in res.fetchall()]
        if 'full_name' in existing_cols:
            with op.batch_alter_table('users') as batch_op:
                batch_op.drop_column('full_name')


def downgrade() -> None:
    conn = op.get_bind()
    res = conn.execute(sa.text("PRAGMA table_info('users')"))
    existing_cols = [r[1] for r in res.fetchall()]

    # Recreate full_name only if it doesn't exist
    if 'full_name' not in existing_cols:
        with op.batch_alter_table('users') as batch_op:
            batch_op.add_column(sa.Column('full_name', sa.String(), nullable=False, server_default=''))

    # Populate full_name from first_name and last_name if those columns exist
    existing_cols = [r[1] for r in conn.execute("PRAGMA table_info('users')").fetchall()]
    if 'first_name' in existing_cols or 'last_name' in existing_cols:
        op.execute(sa.text(
            """
            UPDATE users
            SET full_name = CASE
                WHEN (last_name IS NULL OR trim(last_name) = '') THEN trim(coalesce(first_name, ''))
                ELSE trim(coalesce(first_name, '')) || ' ' || trim(coalesce(last_name, ''))
            END;
            """
        ))

    # Drop the split columns if they exist
    res = conn.execute(sa.text("PRAGMA table_info('users')"))
    existing_cols = [r[1] for r in res.fetchall()]
    with op.batch_alter_table('users') as batch_op:
        if 'first_name' in existing_cols:
            batch_op.drop_column('first_name')
        if 'last_name' in existing_cols:
            batch_op.drop_column('last_name')
