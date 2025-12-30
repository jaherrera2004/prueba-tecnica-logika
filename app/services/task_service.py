from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging
from app.models.task_model import Task
from app.schemas.task_schema import TaskCreate, TaskUpdate
from typing import List, Optional

logger = logging.getLogger(__name__)


def create_task(db: Session, task_data: TaskCreate, user_id: int) -> Task:

    logger.info(f"Creando tarea '{task_data.title}' para usuario {user_id}")
    
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        due_date=task_data.due_date,
        user_id=user_id
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    logger.info(f"Tarea creada exitosamente (ID: {new_task.id}) para usuario {user_id}")
    return new_task


def get_task_by_id(db: Session, task_id: int, user_id: int) -> Task:
    logger.debug(f"Buscando tarea ID {task_id} para usuario {user_id}")
    
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()
    
    if not task:
        logger.warning(f"Tarea no encontrada o no pertenece al usuario (ID: {task_id}, Usuario: {user_id})")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarea no encontrada"
        )
    
    logger.debug(f"Tarea encontrada: ID {task_id}")
    return task


def get_user_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100, status_filter: Optional[str] = None) -> tuple[List[Task], int]:
    logger.debug(f"Consultando tareas para usuario {user_id} (skip: {skip}, limit: {limit}, filtro: {status_filter})")
    
    query = db.query(Task).filter(Task.user_id == user_id)
    
    # Filtrar por status si se proporciona
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    total = query.count()
    tasks = query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    logger.debug(f"Retornando {len(tasks)} tareas de {total} totales para usuario {user_id}")
    return tasks, total


def update_task(db: Session, task_id: int, task_data: TaskUpdate, user_id: int) -> Task:
    """Actualizar una tarea"""
    logger.info(f"Actualizando tarea ID {task_id} para usuario {user_id}")
    
    task = get_task_by_id(db, task_id, user_id)
    
    # Actualizar solo los campos proporcionados
    updated_fields = []
    if task_data.title is not None:
        task.title = task_data.title
        updated_fields.append("title")
    if task_data.description is not None:
        task.description = task_data.description
        updated_fields.append("description")
    if task_data.status is not None:
        task.status = task_data.status
        updated_fields.append("status")
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
        updated_fields.append("due_date")
    
    db.commit()
    db.refresh(task)
    
    logger.info(f"Tarea {task_id} actualizada exitosamente. Campos modificados: {', '.join(updated_fields) if updated_fields else 'ninguno'}")
    return task


def delete_task(db: Session, task_id: int, user_id: int) -> None:

    logger.info(f"Eliminando tarea ID {task_id} para usuario {user_id}")
    
    task = get_task_by_id(db, task_id, user_id)
    
    db.delete(task)
    db.commit()
    
    logger.info(f"Tarea {task_id} eliminada exitosamente")


def get_all_tasks(db: Session, skip: int = 0, limit: int = 100, status_filter: Optional[str] = None) -> tuple[List[Task], int]:

    logger.debug(f"Consultando todas las tareas (skip: {skip}, limit: {limit}, filtro: {status_filter})")
    
    query = db.query(Task)
    
    # Filtrar por status si se proporciona
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    total = query.count()
    tasks = query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    logger.debug(f"Retornando {len(tasks)} tareas de {total} totales (todas las tareas)")
    return tasks, total
