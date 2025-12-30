from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
import logging
from app.db.session import get_db
from app.schemas.user_schema import UserRegister, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import create_user, authenticate_user, get_user_by_id
from app.core.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user_id

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):

    logger.info(f"Intento de registro para el email: {user_data.email}")
    
    user = create_user(db, user_data)
    logger.info(f"Usuario registrado exitosamente: {user.email} (ID: {user.id})")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):

    logger.info(f"Intento de login para el email: {credentials.email}")
    
    user = authenticate_user(db, credentials.email, credentials.password)
    logger.info(f"Login exitoso para el usuario: {user.email} (ID: {user.id})")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
        
    )
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    
    logger.info(f"Intento de renovacion de token para el usuario ID: {user_id}")
    user = get_user_by_id(db, user_id)
    
    if not user:
        logger.warning(f"Intento de renovacion fallido: usuario no encontrado (ID: {user_id})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    # Crear nuevo token con la misma expiracion configurada
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    logger.info(f"Token renovado exitosamente para: {user.email} (ID: {user.id})")
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )
