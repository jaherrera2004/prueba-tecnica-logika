from sqlalchemy.orm import Session
import logging
from app.models.user_model import User
from app.schemas.user_schema import UserRegister
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


def create_user(db: Session, user_data: UserRegister) -> User:
    logger.info(f"Creando usuario con email: {user_data.email}")
    
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        logger.warning(f"Intento de registro con email duplicado: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya esta registrado"
        )
    
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        name=user_data.name,
        lastname=user_data.lastname,
        email=user_data.email,
        password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.info(f"Usuario creado exitosamente: {new_user.email} (ID: {new_user.id})")
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> User:
    logger.info(f"Autenticando usuario: {email}")
    
    user = db.query(User).filter(User.email == email).first()

    if not user:
        logger.warning(f"Intento de login fallido: usuario no existe ({email})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not verify_password(password, user.password):
        logger.warning(f"Intento de login fallido: contrasena incorrecta ({email})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    logger.info(f"Usuario autenticado exitosamente: {user.email} (ID: {user.id})")
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    """Obtener un usuario por su ID"""
    logger.debug(f"Buscando usuario por ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    
    if user:
        logger.debug(f"Usuario encontrado: {user.email} (ID: {user.id})")
    else:
        logger.warning(f"Usuario no encontrado (ID: {user_id})")
    
    return user

