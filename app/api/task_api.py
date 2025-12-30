from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging
from app.db.session import get_db
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.services.task_service import (
    create_task,
    get_task_by_id,
    get_user_tasks,
    update_task,
    delete_task,
    get_all_tasks
)
from app.core.auth import get_current_user_id

logger = logging.getLogger(__name__)
router = APIRouter()

""" NOTA: El usuario debe estar autenticado para todas las operaciones de sus tareas """

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    logger.info(f"Usuario {user_id} creando nueva tarea: {task_data.title}")
    task = create_task(db, task_data, user_id)
    logger.info(f"Tarea creada exitosamente (ID: {task.id}) para usuario {user_id}")
    return task


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    page: int = Query(1, ge=1, description="Numero de pagina"),
    page_size: int = Query(10, ge=1, le=100, description="Cantidad de registros por pagina"),
    status_filter: Optional[str] = Query(None, description="Filtrar por status: pending, in_progress, completed"),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    
    logger.info(f"Usuario {user_id} consultando tareas - Pagina: {page}, Filtro: {status_filter}")
    skip = (page - 1) * page_size

    tasks, total = get_user_tasks(db, user_id, skip, page_size, status_filter)

    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    logger.debug(f"Retornando {len(tasks)} tareas de {total} totales para usuario {user_id}")

    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/all", response_model=TaskListResponse)
async def list_all_tasks(
    page: int = Query(1, ge=1, description="Numero de pagina"),
    page_size: int = Query(10, ge=1, le=100, description="Cantidad de registros por pagina"),
    status_filter: Optional[str] = Query(None, description="Filtrar por status: pending, in_progress, completed, overdue"),
    db: Session = Depends(get_db)
):

    logger.info(f"Consulta de todas las tareas - Pagina: {page}, Filtro: {status_filter}")
    skip = (page - 1) * page_size

    tasks, total = get_all_tasks(db, skip, page_size, status_filter)

    total_pages = (total + page_size - 1) // page_size if total > 0 else 0
    logger.debug(f"Retornando {len(tasks)} tareas de {total} totales (todas las tareas)")

    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    
    logger.info(f"Usuario {user_id} consultando tarea ID: {task_id}")
    task = get_task_by_id(db, task_id, user_id)

    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):

    logger.info(f"Usuario {user_id} actualizando tarea ID: {task_id}")
    task = update_task(db, task_id, task_data, user_id)

    logger.info(f"Tarea {task_id} actualizada exitosamente por usuario {user_id}")

    return task


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
async def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):

    logger.info(f"Usuario {user_id} eliminando tarea ID: {task_id}")
    delete_task(db, task_id, user_id)
  
    logger.info(f"Tarea {task_id} eliminada exitosamente por usuario {user_id}")
    
    return {"message": "Tarea eliminada con exito", "task_id": task_id}
