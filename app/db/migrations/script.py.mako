"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    """
    Aplicar cambios a la base de datos.
    Ejecuta cuando corres: alembic upgrade head
    """
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """
    Revertir cambios de la base de datos.
    Ejecuta cuando corres: alembic downgrade -1
    """
    ${downgrades if downgrades else "pass"}
