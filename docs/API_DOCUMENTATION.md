# Documentación de la API

API REST para gestión de tareas con autenticación JWT.

**Base URL**: `http://localhost:8000`

---

## Autenticación

Todos los endpoints de tareas requieren autenticación mediante JWT Bearer Token.

### 1. Login

Obtener token de acceso.

**Endpoint**: `POST /api/v1/auth/login`

**Body**:
```json
{
  "email": "pepito.perez@test.com",
  "password": "admin123"
}
```

**Respuesta exitosa** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Pepito",
    "lastname": "Pérez",
    "email": "pepito.perez@test.com"
  }
}
```

**Errores**:
- `401 Unauthorized`: Credenciales inválidas
- `422 Unprocessable Entity`: Formato de datos incorrecto

---

### 2. Registro

Crear una nueva cuenta de usuario.

**Endpoint**: `POST /api/v1/auth/register`

**Body**:
```json
{
  "name": "Juan",
  "lastname": "Pérez",
  "email": "juan@example.com",
  "password": "password123"
}
```

**Respuesta exitosa** (201):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 4,
    "name": "Juan",
    "lastname": "Pérez",
    "email": "juan@example.com"
  }
}
```

**Errores**:
- `400 Bad Request`: Email ya registrado
- `422 Unprocessable Entity`: Datos inválidos

---

### 3. Renovar Token (Refresh)

Renovar el token de acceso sin necesidad de hacer login nuevamente.

**Endpoint**: `POST /api/v1/auth/refresh`

**Headers requeridos**:
```
Authorization: Bearer {tu_token_actual}
```

**Body**: No requiere body

**Respuesta exitosa** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "Pepito",
    "lastname": "Pérez",
    "email": "pepito.perez@test.com"
  }
}
```

**Errores**:
- `401 Unauthorized`: Token inválido, expirado o usuario no encontrado

**Nota**: Este endpoint permite renovar el token antes de que expire, manteniendo la sesión del usuario activa sin requerir credenciales.

---

## Gestión de Tareas

### Headers requeridos
Todos los endpoints de tareas requieren:
```
Authorization: Bearer {tu_token}
Content-Type: application/json
```

---

### 4. Listar Tareas

Obtener todas las tareas del usuario autenticado con paginación.

**Endpoint**: `GET /api/v1/tasks`

**Query Parameters**:
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `page` | integer | No | `1` | Número de página (mínimo: 1) |
| `page_size` | integer | No | `10` | Registros por página (1-100) |
| `status_filter` | string | No | - | Filtrar por estado |

**Valores válidos para `status_filter`**:
- `pending` - Tareas pendientes
- `in_progress` - En progreso
- `completed` - Completadas
- `overdue` - Vencidas

**Ejemplo de petición**:
```bash
GET /api/v1/tasks?page=1&page_size=10&status_filter=pending
```

**Respuesta exitosa** (200):
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Implementar autenticación",
      "description": "Crear sistema de login con JWT",
      "status": "completed",
      "user_id": 1,
      "due_date": "2025-12-31T23:59:59Z",
      "created_at": "2025-12-20T10:00:00Z"
    },
    {
      "id": 2,
      "title": "Documentar API",
      "description": "Crear documentación completa",
      "status": "in_progress",
      "user_id": 1,
      "due_date": null,
      "created_at": "2025-12-21T11:30:00Z"
    }
  ],
  "total": 8,
  "page": 1,
  "page_size": 10,
  "total_pages": 1
}
```

**Errores**:
- `401 Unauthorized`: Token inválido o expirado

---

### 5. Obtener Tarea por ID

Obtener los detalles de una tarea específica.

**Endpoint**: `GET /api/v1/tasks/{task_id}`

**Path Parameters**:
- `task_id` (integer): ID de la tarea

**Ejemplo**:
```bash
GET /api/v1/tasks/1
```

**Respuesta exitosa** (200):
```json
{
  "id": 1,
  "title": "Implementar autenticación",
  "description": "Crear sistema de login con JWT",
  "status": "completed",
  "user_id": 1,
  "due_date": "2025-12-31T23:59:59Z",
  "created_at": "2025-12-20T10:00:00Z"
}
```

**Errores**:
- `404 Not Found`: Tarea no encontrada o no pertenece al usuario
- `401 Unauthorized`: Token inválido

---

### 6. Crear Tarea

Crear una nueva tarea para el usuario autenticado.

**Endpoint**: `POST /api/v1/tasks`

**Body**:
```json
{
  "title": "Nueva tarea",
  "description": "Descripción detallada (opcional)",
  "status": "pending",
  "due_date": "2025-12-31T23:59:59Z"
}
```

**Campos**:
| Campo | Tipo | Requerido | Default | Descripción |
|-------|------|-----------|---------|-------------|
| `title` | string | **Sí** | - | Título (1-255 caracteres) |
| `description` | string | No | `null` | Descripción de la tarea |
| `status` | enum | No | `pending` | Estado de la tarea |
| `due_date` | datetime | No | `null` | Fecha de vencimiento (ISO 8601) |

**Respuesta exitosa** (201):
```json
{
  "id": 9,
  "title": "Nueva tarea",
  "description": "Descripción detallada",
  "status": "pending",
  "user_id": 1,
  "due_date": "2025-12-31T23:59:59Z",
  "created_at": "2025-12-29T15:30:00Z"
}
```

**Errores**:
- `422 Unprocessable Entity`: Datos inválidos (título vacío, status inválido, etc.)
- `401 Unauthorized`: Token inválido

---

### 7. Actualizar Tarea

Actualizar una tarea existente. Todos los campos son opcionales.

**Endpoint**: `PUT /api/v1/tasks/{task_id}`

**Path Parameters**:
- `task_id` (integer): ID de la tarea

**Body** (todos los campos opcionales):
```json
{
  "title": "Título actualizado",
  "description": "Nueva descripción",
  "status": "completed",
  "due_date": "2026-01-15T12:00:00Z"
}
```

**Ejemplo de actualización parcial**:
```json
{
  "status": "completed"
}
```

**Respuesta exitosa** (200):
```json
{
  "id": 1,
  "title": "Título actualizado",
  "description": "Nueva descripción",
  "status": "completed",
  "user_id": 1,
  "due_date": "2026-01-15T12:00:00Z",
  "created_at": "2025-12-20T10:00:00Z"
}
```

**Errores**:
- `404 Not Found`: Tarea no encontrada
- `422 Unprocessable Entity`: Datos inválidos
- `401 Unauthorized`: Token inválido

---

### 8. Eliminar Tarea

Eliminar una tarea del usuario autenticado.

**Endpoint**: `DELETE /api/v1/tasks/{task_id}`

**Path Parameters**:
- `task_id` (integer): ID de la tarea

**Ejemplo**:
```bash
DELETE /api/v1/tasks/1
```

**Respuesta exitosa** (200):
```json
{
  "message": "Tarea eliminada con éxito",
  "task_id": 1
}
```

**Errores**:
- `404 Not Found`: Tarea no encontrada
- `401 Unauthorized`: Token inválido

---

### 9. Listar Todas las Tareas (Admin)

Obtener todas las tareas de todos los usuarios (sin filtro de usuario).

**Endpoint**: `GET /api/v1/tasks/all/tasks`

**Query Parameters**:
| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `page` | integer | No | `1` | Número de página |
| `page_size` | integer | No | `10` | Registros por página (1-100) |
| `status_filter` | string | No | - | Filtrar por estado |

**Ejemplo**:
```bash
GET /api/v1/tasks/all/tasks?page=1&page_size=10
```

**Respuesta exitosa** (200):
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Tarea usuario 1",
      "description": "...",
      "status": "completed",
      "user_id": 1,
      "due_date": null,
      "created_at": "2025-12-20T10:00:00Z"
    },
    {
      "id": 5,
      "title": "Tarea usuario 2",
      "description": "...",
      "status": "pending",
      "user_id": 2,
      "due_date": null,
      "created_at": "2025-12-24T08:00:00Z"
    }
  ],
  "total": 11,
  "page": 1,
  "page_size": 10,
  "total_pages": 2
}
```

---

## Modelos de Datos

### TaskStatus (Enum)
```
- pending: Tarea pendiente
- in_progress: Tarea en progreso
- completed: Tarea completada
- overdue: Tarea vencida
```

### Task
```json
{
  "id": integer,
  "title": string (1-255 caracteres),
  "description": string | null,
  "status": TaskStatus,
  "user_id": integer,
  "due_date": datetime (ISO 8601) | null,
  "created_at": datetime (ISO 8601)
}
```

### User
```json
{
  "id": integer,
  "name": string,
  "lastname": string,
  "email": string (email válido)
}
```

---

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| `200` | Operación exitosa |
| `201` | Recurso creado exitosamente |
| `400` | Petición inválida (ej: email duplicado) |
| `401` | No autenticado o token inválido |
| `404` | Recurso no encontrado |
| `422` | Datos de entrada inválidos (validación fallida) |
| `500` | Error interno del servidor |

---

## Ejemplos con cURL

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "pepito.perez@test.com",
    "password": "admin123"
  }'
```

### Renovar Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Authorization: Bearer YOUR_CURRENT_TOKEN"
```

### Crear Tarea
```bash
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Implementar feature X",
    "description": "Descripción completa",
    "status": "pending"
  }'
```

### Listar Tareas (Página 2)
```bash
curl -X GET "http://localhost:8000/api/v1/tasks?page=2&page_size=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Actualizar Estado
```bash
curl -X PUT http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Eliminar Tarea
```bash
curl -X DELETE http://localhost:8000/api/v1/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Recursos Adicionales

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Notas

1. **JWT Expiración**: Los tokens expiran en 30 minutos (configurable en `.env.local`)
2. **Paginación**: El máximo de registros por página es 100
3. **Fecha/Hora**: Usar formato ISO 8601 (ej: `2025-12-31T23:59:59Z`)
4. **Email**: Debe ser un email válido y único en el sistema
5. **Contraseñas**: Se almacenan hasheadas con bcrypt

---

**Última actualización**: Diciembre 29, 2025
