"""Crear tablas users y tasks con datos iniciales

Revision ID: 001
Revises: 
Create Date: 2025-12-29

Esta migración crea:
1. Tabla users (usuarios del sistema)
2. Tabla tasks (tareas de los usuarios)
3. Usuario inicial obligatorio (admin@test.com)
4. Datos de ejemplo (3 tareas de prueba)
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime
import bcrypt
import logging


logger = logging.getLogger("alembic.runtime.migration")


# Identificadores de revisión
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Crear las tablas y los datos iniciales.
    Esta función se ejecuta cuando corres: alembic upgrade head
    """
    
    logger.info("[001] Iniciando migración: creación de tablas + seed")

    # ========================================
    # 1. CREAR TABLA USERS
    # ========================================
    logger.info("[001] Creando tabla 'users'")
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('lastname', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices en users
    logger.info("[001] Creando índices de 'users'")
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    
    # ========================================
    # 2. CREAR TABLA TASKS
    # ========================================
    logger.info("[001] Creando tabla 'tasks'")
    op.create_table(
        'tasks',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', 'overdue', name='taskstatus'), nullable=False),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices en tasks
    logger.info("[001] Creando índices de 'tasks'")
    op.create_index('ix_tasks_id', 'tasks', ['id'], unique=False)
    op.create_index('ix_tasks_user_id', 'tasks', ['user_id'], unique=False)
    
    # ========================================
    # 3. INSERTAR USUARIO INICIAL (OBLIGATORIO)
    # ========================================
    logger.info("[001] Insertando usuario inicial obligatorio")
    
    # Hashear la contraseña de forma segura
    password = "admin123"
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Definir la estructura de la tabla para inserción
    users_table = table(
        'users',
        column('id', sa.BigInteger),
        column('name', sa.String),
        column('lastname', sa.String),
        column('email', sa.String),
        column('password', sa.String)
    )
    
    # Insertar el usuario inicial obligatorio
    op.bulk_insert(
        users_table,
        [
            {
                'id': 1,
                'name': 'Pepito',
                'lastname': 'Pérez',
                'email': 'pepito.perez@test.com',
                'password': password_hash
            }
        ]
    )
    
    # ========================================
    # 4. INSERTAR DATOS DE EJEMPLO (SEED DATA)
    # ========================================
    logger.info("[001] Insertando usuarios seed adicionales")
    
    # Insertar 2 usuarios más de prueba
    password_user = "user123"
    password_user_hash = bcrypt.hashpw(password_user.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    op.bulk_insert(
        users_table,
        [
            {
                'id': 2,
                'name': 'María',
                'lastname': 'García',
                'email': 'maria.garcia@test.com',
                'password': password_user_hash
            },
            {
                'id': 3,
                'name': 'Juan',
                'lastname': 'López',
                'email': 'juan.lopez@test.com',
                'password': password_user_hash
            }
        ]
    )
    
    # Definir la estructura de la tabla tasks para inserción
    tasks_table = table(
        'tasks',
        column('id', sa.BigInteger),
        column('title', sa.String),
        column('description', sa.Text),
        column('user_id', sa.BigInteger),
        column('status', sa.String),
        column('created_at', sa.DateTime)
    )
    
    # Insertar 8 tareas de ejemplo con diferentes estados
    logger.info("[001] Insertando tareas seed")
    op.bulk_insert(
        tasks_table,
        [
            {
                'id': 1,
                'title': 'Configurar entorno de desarrollo',
                'description': 'Instalar Docker, Python y dependencias necesarias',
                'user_id': 1,
                'status': 'completed',
                'created_at': datetime(2025, 12, 20, 10, 0, 0)
            },
            {
                'id': 2,
                'title': 'Implementar autenticación JWT',
                'description': 'Crear endpoints de login y registro con tokens JWT',
                'user_id': 1,
                'status': 'completed',
                'created_at': datetime(2025, 12, 21, 11, 30, 0)
            },
            {
                'id': 3,
                'title': 'Crear CRUD de tareas',
                'description': 'Implementar endpoints para crear, leer, actualizar y eliminar tareas',
                'user_id': 1,
                'status': 'in_progress',
                'created_at': datetime(2025, 12, 22, 9, 15, 0)
            },
            {
                'id': 4,
                'title': 'Documentar API con Swagger',
                'description': 'Agregar documentación automática de todos los endpoints',
                'user_id': 1,
                'status': 'pending',
                'created_at': datetime(2025, 12, 23, 14, 45, 0)
            },
            {
                'id': 5,
                'title': 'Revisar código del proyecto',
                'description': 'Hacer code review y refactorizar donde sea necesario',
                'user_id': 2,
                'status': 'in_progress',
                'created_at': datetime(2025, 12, 24, 8, 0, 0)
            },
            {
                'id': 6,
                'title': 'Preparar presentación',
                'description': 'Crear slides para la demostración del proyecto',
                'user_id': 2,
                'status': 'pending',
                'created_at': datetime(2025, 12, 25, 16, 20, 0)
            },
            {
                'id': 7,
                'title': 'Escribir tests unitarios',
                'description': 'Crear tests para los servicios principales',
                'user_id': 3,
                'status': 'pending',
                'created_at': datetime(2025, 12, 26, 10, 30, 0)
            },
            {
                'id': 8,
                'title': 'Configurar CI/CD',
                'description': 'Implementar pipeline de integración continua con GitHub Actions',
                'user_id': 3,
                'status': 'completed',
                'created_at': datetime(2025, 12, 27, 13, 0, 0)
            }
        ]
    )

    logger.info("[001] Migración completada exitosamente")


def downgrade() -> None:
    """
    Revertir los cambios de esta migración.
    Esta función se ejecuta cuando corres: alembic downgrade -1
    """
    
    logger.info("[001] Revirtiendo migración: eliminando tablas e índices")

    # Eliminar las tablas en orden inverso (por las foreign keys)
    op.drop_index('ix_tasks_user_id', table_name='tasks')
    op.drop_index('ix_tasks_id', table_name='tasks')
    op.drop_table('tasks')
    
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')

    logger.info("[001] Downgrade completado")
