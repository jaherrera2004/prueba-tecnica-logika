"""
Configuración del entorno de Alembic
Este archivo se ejecuta cada vez que corres un comando de Alembic
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Importar la configuración de la aplicación
from app.core.config import settings
from app.db.session import Base

# Importar todos los modelos para que Alembic los detecte
from app.models.user_model import User
from app.models.task_model import Task

# Configuración de Alembic
config = context.config

# Interpretar el archivo de configuración para el logger de Python
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Agregar los metadatos de los modelos para detección automática
target_metadata = Base.metadata

# =====================================================================
# FUNCIONES DE MIGRACIÓN
# =====================================================================

def run_migrations_offline() -> None:
    """
    Ejecutar migraciones en modo 'offline'.
    
    En este modo, no necesitamos una conexión real a la base de datos.
    Solo genera SQL scripts.
    """
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Ejecutar migraciones en modo 'online'.
    
    En este modo, necesitamos una conexión real a la base de datos.
    Es el modo normal cuando ejecutas 'alembic upgrade head'.
    """
    # Crear la configuración del engine usando la URL de la base de datos
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Detectar el modo y ejecutar la función correspondiente
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
