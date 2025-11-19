"""
Endpoints de Autenticación
Login, logout, refresh token, 2FA
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest
from app.schemas.user import UserCreate, User
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password
)
from app.core.config import settings
from app.models.user import User as UserModel
from app.models.audit_log import log_action

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ============================================
# DEPENDENCIES
# ============================================

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UserModel:
    """
    Obtiene el usuario actual desde el token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    return user


# ============================================
# ENDPOINTS
# ============================================

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registrar nuevo usuario

    GDPR: Obtener consentimiento antes de crear cuenta
    """
    # Verificar si el email ya existe
    existing_user = db.query(UserModel).filter(
        UserModel.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Verificar si el username ya existe
    existing_username = db.query(UserModel).filter(
        UserModel.username == user_data.username
    ).first()

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )

    # Crear usuario
    hashed_password = hash_password(user_data.password)

    new_user = UserModel(
        email=user_data.email,
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=user_data.role,
        hashed_password=hashed_password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Registrar en audit log
    log_action(
        db=db,
        user_id=new_user.id,
        user_email=new_user.email,
        user_role=new_user.role.value,
        action="USER_REGISTERED",
        status="SUCCESS",
        resource_type="User",
        resource_id=new_user.id
    )

    return new_user


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login de usuario

    LOPDGDD: Registrar acceso en audit log
    """
    # Buscar usuario
    user = db.query(UserModel).filter(
        UserModel.email == login_data.email
    ).first()

    if not user or not verify_password(login_data.password, user.hashed_password):
        # Registrar intento fallido
        if user:
            log_action(
                db=db,
                user_id=user.id,
                user_email=user.email,
                user_role=user.role.value,
                action="LOGIN_FAILED",
                status="FAILED",
                error_message="Contraseña incorrecta"
            )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    # Verificar 2FA si está habilitado
    if user.is_2fa_enabled and not login_data.totp_code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere código 2FA"
        )

    # Crear tokens
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email, "role": user.role.value}
    )

    refresh_token = create_refresh_token(
        data={"user_id": user.id}
    )

    # Actualizar last_login
    from sqlalchemy import func
    user.last_login = func.now()
    db.commit()

    # Registrar login exitoso
    log_action(
        db=db,
        user_id=user.id,
        user_email=user.email,
        user_role=user.role.value,
        action="LOGIN_SUCCESS",
        status="SUCCESS"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refrescar access token usando refresh token
    """
    payload = decode_token(refresh_data.refresh_token)

    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido"
        )

    user_id = payload.get("user_id")
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no válido"
        )

    # Crear nuevo access token
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email, "role": user.role.value}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Logout de usuario

    Nota: Con JWT stateless, el logout es del lado del cliente
    Aquí solo registramos el evento
    """
    log_action(
        db=db,
        user_id=current_user.id,
        user_email=current_user.email,
        user_role=current_user.role.value,
        action="LOGOUT",
        status="SUCCESS"
    )

    return {"message": "Logout exitoso"}


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user)
):
    """
    Obtener información del usuario actual
    """
    return current_user
