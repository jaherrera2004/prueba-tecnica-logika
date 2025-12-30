"""Fix sequences after seed inserts

Revision ID: 002
Revises: 001
Create Date: 2025-12-30

Motivation:
- The initial migration inserts explicit IDs for seed data (users/tasks).
- In PostgreSQL, sequences/identity generators are not automatically advanced by
  explicit inserts, which can cause duplicate key errors on subsequent inserts.

This migration syncs the sequences (if they exist) to MAX(id) for users/tasks.
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def _sync_pk_sequence(table_name: str, pk_column: str = "id") -> None:
    # Works for SERIAL and IDENTITY, but safely no-ops if no sequence exists.
    op.execute(
        f"""
DO $$
DECLARE
    seq_name text;
BEGIN
    seq_name := pg_get_serial_sequence('{table_name}', '{pk_column}');

    IF seq_name IS NULL THEN
        RETURN;
    END IF;

    EXECUTE format(
        'SELECT setval(%L::regclass, COALESCE((SELECT MAX({pk_column}) FROM {table_name}), 1), true);',
        seq_name
    );
END $$;
"""
    )


def upgrade() -> None:
    _sync_pk_sequence("users", "id")
    _sync_pk_sequence("tasks", "id")


def downgrade() -> None:
    # No-op: sequence values are derived from data.
    pass
