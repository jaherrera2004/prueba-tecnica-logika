# Guía de Migraciones con Alembic

Esta guía explica cómo funcionan las migraciones en este proyecto.

## Estructura de Archivos

```
├── alembic.ini                          # Configuración principal de Alembic
└── app/db/migrations/
    ├── env.py                           # Configuración del entorno
    ├── script.py.mako                   # Plantilla para nuevas migraciones
    └── versions/
        └── 001_initial_tables.py        # Primera migración (tablas users y tasks)
```

## Comandos Básicos

### Ver estado actual de migraciones
```bash
alembic current
```

### Aplicar todas las migraciones pendientes
```bash
alembic upgrade head
```

### Revertir la última migración
```bash
alembic downgrade -1
```

### Ver historial de migraciones
```bash
alembic history
```

### Crear una nueva migración automática
```bash
alembic revision --autogenerate -m "descripcion del cambio"
```

### Crear una migración manual
```bash
alembic revision -m "descripcion del cambio"
```

## Migración Inicial: 001_initial_tables.py

La primera migración crea todo lo necesario para que el proyecto funcione:

### 1. Tabla `users`
```sql
- id (BigInteger, Primary Key)
- name (String, NOT NULL)
- lastname (String, NOT NULL)
- email (String, UNIQUE, NOT NULL, INDEXED)
- password (String, NOT NULL)
```

### 2. Tabla `tasks`
```sql
- id (BigInteger, Primary Key)
- title (String, NOT NULL)
- description (Text, NULLABLE)
- user_id (BigInteger, Foreign Key -> users.id)
- status (Enum: pending, in_progress, completed, overdue)
- due_date (DateTime, NULLABLE)
- created_at (DateTime, DEFAULT now())
```

### 3. Usuario Inicial Obligatorio
```
Email: pepito.perez@test.com
Password: admin123 (hasheado con bcrypt)
```

### 4. Datos de Ejemplo (Seed Data)
- 2 usuarios adicionales
- 8 tareas de ejemplo con diferentes estados

## Migraciones en Docker

Cuando inicias el proyecto con Docker Compose, las migraciones se ejecutan automáticamente:

```bash
docker compose up --build
```

El `entrypoint.sh` se encarga de:
1. Esperar a que PostgreSQL esté listo
2. Ejecutar `alembic upgrade head`
3. Iniciar la aplicación FastAPI

## Cómo Crear una Nueva Migración

### Ejemplo: Agregar campo "priority" a tasks

1. **Modificar el modelo** en `app/models/task_model.py`:
```python
class Task(Base):
    # ... campos existentes ...
    priority = Column(String(20), default="medium")
```

2. **Generar migración automática**:
```bash
alembic revision --autogenerate -m "add priority field to tasks"
```

3. **Revisar el archivo generado** en `app/db/migrations/versions/`

4. **Aplicar la migración**:
```bash
alembic upgrade head
```

## Buenas Prácticas

### HACER:
- Revisar siempre las migraciones autogeneradas antes de aplicarlas
- Escribir descripciones claras en los mensajes de commit
- Probar las migraciones en desarrollo antes de producción
- Incluir tanto `upgrade()` como `downgrade()`

### NO HACER:
- Editar migraciones que ya fueron aplicadas en producción
- Eliminar archivos de migración
- Modificar directamente la base de datos (usar migraciones)
- Olvidar hacer backup antes de migraciones importantes

## Solución de Problemas

### Error: "can't locate revision identified by 'XXXX'"
```bash
# Recrear la base de datos y aplicar migraciones desde cero
docker compose down -v
docker compose up --build
```

### Error: "Target database is not up to date"
```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head
```

### Ver qué SQL ejecutará una migración sin aplicarla
```bash
alembic upgrade head --sql
```

## Recursos Adicionales

- [Documentación oficial de Alembic](https://alembic.sqlalchemy.org/)
- [Tutorial de Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Documentación de SQLAlchemy](https://docs.sqlalchemy.org/)

## Resumen Rápido

```bash
# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1

# Crear nueva migración
alembic revision --autogenerate -m "descripcion"

# Ver estado actual
alembic current
```

---

**Nota**: En este proyecto, las migraciones se ejecutan automáticamente cuando inicias Docker Compose, por lo que normalmente no necesitas ejecutar comandos manualmente.
