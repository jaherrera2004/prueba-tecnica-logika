# API de Gestión de Tareas - Prueba Técnica Logika

API REST desarrollada con **FastAPI**, **PostgreSQL**, **SQLAlchemy** y **Alembic** para gestionar tareas y usuarios con autenticación JWT.

## Características

- **Autenticación JWT** con bcrypt (expiración configurable: 30 min)
- **CRUD completo** de tareas con paginación
- **Gestión de usuarios** con validación de email
- **Migraciones Alembic** con usuario inicial automático
- **Docker Compose** con healthcheck de PostgreSQL
- **Seed data** (3 usuarios + 8 tareas de ejemplo)
- **Índices optimizados** en campos de búsqueda frecuente

## Stack Tecnológico

- **Python 3.11.8** - Lenguaje base
- **FastAPI 0.109** - Framework web asíncrono
- **PostgreSQL 15** - Base de datos relacional
- **SQLAlchemy 2.0** - ORM
- **Alembic 1.13** - Migraciones de BD
- **PyJWT 2.8** - Tokens de autenticación
- **Bcrypt 4.1** - Hash seguro de contraseñas

## Estructura del Proyecto

```
.
├── app/
│   ├── api/              # Endpoints de la API
│   │   ├── auth_api.py   # Autenticación
│   │   └── task_api.py   # Gestión de tareas
│   ├── core/             # Configuración y seguridad
│   │   ├── auth.py       # Lógica de autenticación
│   │   ├── config.py     # Configuración
│   │   └── security.py   # Utilidades de seguridad
│   ├── db/               # Base de datos
│   │   ├── session.py    # Sesión de SQLAlchemy
│   │   └── migrations/   # Migraciones de Alembic
│   ├── models/           # Modelos de datos
│   │   ├── user_model.py
│   │   └── task_model.py
│   ├── schemas/          # Esquemas Pydantic
│   │   ├── user_schema.py
│   │   └── task_schema.py
│   ├── services/         # Lógica de negocio
│   │   ├── auth_service.py
│   │   └── task_service.py
│   └── main.py           # Aplicación principal
├── alembic.ini           # Configuración de Alembic
├── docker-compose.yml    # Orquestación de contenedores
├── Dockerfile            # Imagen de la aplicación
├── requirements.txt      # Dependencias Python
├── migrate.sh/.bat       # Scripts de migración
└── docs/
    ├── MIGRATIONS.md     # Guía de migraciones
    ├── API_DOCUMENTATION.md  # Documentación completa de la API
    └── db_diagram.png    # Diagrama de la base de datos

```

## Inicio Rápido

### Prerrequisitos
- Docker & Docker Compose
- Git

### Con Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <url-del-repo>
cd prueba-tecnica-logika
```

2. **Configurar variables de entorno**

El archivo `.env.local` ya está configurado con valores por defecto. Para personalizarlo:

```env
# .env.local (ya incluido)
POSTGRES_USER=root
POSTGRES_PASSWORD=123456
POSTGRES_SERVER=postgres
POSTGRES_PORT=5432
POSTGRES_DB=task_system_logika
SECRET_KEY=tu-secret-key-super-segura-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. **Iniciar con Docker Compose**
```bash
docker compose up --build
```

Esto automáticamente:
- Levanta PostgreSQL con healthcheck
- Construye la imagen de la aplicación
- Ejecuta migraciones de Alembic
- Crea usuario inicial + seed data (11 registros)
- Inicia la API en http://localhost:8000

La API estará lista en aproximadamente 15 segundos.

### Sin Docker

1. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**

Copiar `.env.local` existente o crear uno nuevo:

```env
# .env.local
POSTGRES_USER=root
POSTGRES_PASSWORD=123456
POSTGRES_SERVER=localhost  # localhost para ejecución local
POSTGRES_PORT=5432
POSTGRES_DB=task_system_logika
SECRET_KEY=tu-secret-key-super-segura-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PROJECT_NAME=Logika API
VERSION=1.0.0
```

4. **Levantar PostgreSQL**
```bash
docker compose up postgres -d
```

5. **Ejecutar migraciones**
```bash
# Linux/Mac
./migrate.sh

# Windows
migrate.bat

# O directamente
alembic upgrade head
```

6. **Iniciar la aplicación**
```bash
uvicorn app.main:app --reload
```

La API estará en http://localhost:8000

---

## Documentación

- **[Documentación completa de la API](docs/API_DOCUMENTATION.md)** - Todos los endpoints con ejemplos detallados
- **[Guía de migraciones](docs/MIGRATIONS.md)** - Comandos y buenas prácticas con Alembic
- **[Diagrama de base de datos](docs/db_diagram.png)** - Esquema visual de las tablas y relaciones

---

## Decisiones Técnicas

### 1. **Tabla de Usuarios Independiente**
**Decisión**: Implementar una tabla `users` separada en lugar de manejar tareas sin autenticación.  
**Razón**: Permite asignar tareas a usuarios específicos, facilita la implementación del endpoint `/auth/login`, y habilita features futuras como colaboración entre usuarios, permisos granulares y auditoría. Además, hace que los endpoints de tareas tengan sentido al filtrar por `user_id`, garantizando que cada usuario solo vea sus propias tareas.

### 2. **Autenticación por Email (no username)**
**Decisión**: Usar `email` como identificador de usuario.  
**Razón**: Más intuitivo para usuarios, único por naturaleza, y permite recuperación de contraseña.

### 3. **Índices en Base de Datos**
```sql
-- Índices implementados y justificación:
users.email  → UNIQUE INDEX (búsquedas frecuentes en login)
users.id     → PRIMARY KEY INDEX (joins con tasks)
tasks.id     → PRIMARY KEY INDEX (acceso directo)
tasks.user_id → INDEX (filtrado por usuario, muy frecuente)
```
**Razón**: Optimiza consultas más comunes (login, listado de tareas por usuario).

### 4. **Paginación con page/page_size**
**Decisión**: Parámetros `page` (número de página) y `page_size` (registros por página).  
**Razón**: Más intuitivo para usuarios finales, fácil de entender y navegar entre páginas.

**Ejemplo**:
```bash
GET /api/v1/tasks?page=1&page_size=10    # Primera página (registros 1-10)
GET /api/v1/tasks?page=2&page_size=10    # Segunda página (registros 11-20)
GET /api/v1/tasks?page=3&page_size=5     # Tercera página con 5 registros
```

**Response**:
```json
{
  "tasks": [...],
  "total": 50,
  "page": 1,
  "page_size": 10,
  "total_pages": 5
}
```

### 5. **Hash de Contraseñas con Bcrypt**
**Decisión**: Bcrypt con salt automático.  
**Razón**: Algoritmo probado, resistente a rainbow tables, salt único por contraseña.

### 6. **Expiración de JWT Configurable**
**Decisión**: Variable `ACCESS_TOKEN_EXPIRE_MINUTES=30` en `.env.local`.  
**Razón**: Permite ajustar seguridad vs conveniencia según entorno (dev: 60 min, prod: 15 min).

### 7. **Estados de Task**
```python
TaskStatus = Enum("pending", "in_progress", "completed", "overdue")
```
**Decisión**: 4 estados en lugar de 3.  
**Razón**: Agregué `overdue` para manejar tareas vencidas sin perder información del estado original.

### 8. **Arquitectura en Capas**
```
API (routers) → Services (lógica) → Models (ORM) → DB
```
**Razón**: Separación de responsabilidades, testeable, escalable. Servicios reutilizables desde múltiples endpoints.

### 9. **Migraciones con Seed Data**
**Decisión**: Usuario inicial + 8 tareas en misma migración.  
**Razón**: Garantiza entorno funcional desde el primer `docker compose up`. No requiere scripts adicionales.

### 10. **Docker Healthcheck**
**Decisión**: App espera a que PostgreSQL pase healthcheck.  
**Razón**: Evita errores de "connection refused" durante inicio. Garantiza orden correcto de arranque.

---

## Credenciales de Prueba

Usuario inicial creado automáticamente en migración `001_initial_tables.py`:

| Email | Password | Creación |
|-------|----------|----------|
| **pepito.perez@test.com** | **admin123** | Automática (requerido) |
| maria.garcia@test.com | user123 | Seed data |
| juan.lopez@test.com | user123 | Seed data |

**Seed data**: 8 tareas distribuidas entre los 3 usuarios con diferentes estados.

---

## Documentación de la API

Una vez iniciada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Documentación detallada**: [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

## Autenticación

### 1. Login
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "pepito.perez@test.com",
  "password": "admin123"
}
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 2. Usar el token

Incluir en las peticiones el header:
```
Authorization: Bearer <tu-token>
```

## Endpoints de la API

### Autenticación (público)
- `POST /api/v1/auth/login` - Login con email/password
- `POST /api/v1/auth/register` - Crear nueva cuenta

### Tareas (requiere JWT)
- `GET /api/v1/tasks?page=1&page_size=10&status_filter=pending` - Listar con paginación
- `POST /api/v1/tasks` - Crear tarea
- `GET /api/v1/tasks/{id}` - Detalle de tarea
- `PUT /api/v1/tasks/{id}` - Actualizar tarea (campos opcionales)
- `DELETE /api/v1/tasks/{id}` - Eliminar tarea

**Filtros disponibles**: `status_filter` → `pending` | `in_progress` | `completed` | `overdue`

**Nota**: Para ver todos los endpoints con ejemplos detallados, consultar [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)

---

## Migraciones

Alembic maneja la estructura de BD automáticamente. Ver [MIGRATIONS.md](docs/MIGRATIONS.md) para detalles completos.

```bash
alembic upgrade head     # Aplicar todas las migraciones
alembic current          # Ver versión actual
alembic downgrade -1     # Revertir última migración
```

---

## Docker Compose

```bash
docker compose up --build      # Iniciar (primera vez)
docker compose up -d           # Iniciar en background
docker compose down            # Detener
docker compose logs -f app     # Ver logs de la API
docker compose exec app bash   # Entrar al contenedor
```

---

## Ejemplos de Uso (curl)

### 1. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"pepito.perez@test.com","password":"admin123"}'
```

### 2. Crear tarea
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Implementar feature X","status":"pending"}'
```

### 3. Listar tareas paginadas
```bash
curl "http://localhost:8000/api/v1/tasks?page=1&page_size=5&status_filter=pending" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Respuesta**:
```json
{
  "tasks": [...],
  "total": 50,
  "page": 1,
  "page_size": 5,
  "total_pages": 10
}
```

### 4. Actualizar tarea
```bash
curl -X PUT http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'
```

**Swagger disponible en**: http://localhost:8000/docs

---

## Variables de Entorno (.env.local)

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `POSTGRES_USER` | Usuario de PostgreSQL | `root` |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL | `123456` |
| `POSTGRES_SERVER` | Host de PostgreSQL | `postgres` (Docker) / `localhost` (local) |
| `POSTGRES_PORT` | Puerto de PostgreSQL | `5432` |
| `POSTGRES_DB` | Nombre de la base de datos | `task_system_logika` |
| `SECRET_KEY` | Clave para firmar JWT | (cambiar en producción) |
| `ALGORITHM` | Algoritmo JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración del token | `30` minutos |

---

## Dependencias

```txt
fastapi==0.109.0          # Framework web asíncrono
uvicorn==0.27.0           # Servidor ASGI
sqlalchemy==2.0.25        # ORM
alembic==1.13.1           # Migraciones de BD
psycopg2-binary==2.9.9    # Driver PostgreSQL
pydantic==2.5.3           # Validación de datos
PyJWT==2.8.0              # Tokens JWT
bcrypt==4.1.3             # Hash de contraseñas
```

---

**Beneficios**: Testeable, escalable, desacoplado. Servicios reutilizables desde cualquier endpoint.

### Diagrama de Base de Datos

![Diagrama de Base de Datos](./docs/db_diagram.png)

El diagrama muestra:
- **Tabla `users`**: Almacena credenciales y datos de autenticación (id, name, lastname, email, password)
- **Tabla `tasks`**: Gestiona tareas con relación a usuarios (id, title, description, status, user_id, due_date, created_at)
- **Relación 1:N**: Un usuario puede tener múltiples tareas (clave foránea `user_id`)
- **Índices**: Destacados para optimizar búsquedas por email y filtrado por usuario

---

## Recursos

- [Swagger UI](http://localhost:8000/docs) - Documentación interactiva
- [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - Documentación completa de endpoints
- [MIGRATIONS.md](docs/MIGRATIONS.md) - Guía de migraciones
- [Diagrama de Base de Datos](docs/db_diagram.png) - Esquema visual
- [FastAPI Docs](https://fastapi.tiangolo.com/) - Documentación oficial de FastAPI

---

**Desarrollado para Prueba Técnica Logika**
