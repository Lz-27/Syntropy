from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.models.user import User
from app.models.audit import AuditoriaLog
from app.schemas.user import UserCreate, UserOut, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def _log(db: Session, accion: str, usuario_id=None, ip=None, detalle=None):
    db.add(AuditoriaLog(accion=accion, usuario_id=usuario_id, ip=ip, detalle=detalle))
    db.commit()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(body: UserCreate, request: Request, db: Session = Depends(get_db)):
    """Registra un nuevo usuario estudiante."""
    # Verificar duplicados
    existing = db.query(User).filter(
        or_(User.email == body.email, User.codigo_estudiante == body.codigo_estudiante)
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo o código de estudiante ya está registrado",
        )

    user = User(
        nombre_completo=body.nombre_completo,
        codigo_estudiante=body.codigo_estudiante,
        email=body.email,
        password_hash=hash_password(body.password),
        rol="estudiante",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    ip = request.client.host if request.client else None
    _log(db, "register", usuario_id=user.id, ip=ip, detalle=f"nuevo usuario: {user.email}")
    return user


import time
from collections import defaultdict

_failed_attempts = defaultdict(list)


def _check_rate_limit(key: str, max_attempts: int = 5, window_seconds: int = 60):
    now = time.time()
    attempts = [t for t in _failed_attempts[key] if now - t < window_seconds]
    _failed_attempts[key] = attempts
    if len(attempts) >= max_attempts:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Demasiados intentos fallidos. Por favor espera {int(window_seconds - (now - attempts[0]))} segundos.",
        )


def _record_failed_attempt(key: str):
    _failed_attempts[key].append(time.time())


@router.post("/login", response_model=TokenResponse)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Autenticación con email/código + contraseña. Retorna JWT (con rate limiting de seguridad)."""
    ip = request.client.host if request.client else "unknown"
    rate_key = f"{ip}:{form_data.username}"
    _check_rate_limit(rate_key)

    # Buscar por email O código de estudiante
    user = db.query(User).filter(
        or_(
            User.email == form_data.username,
            User.codigo_estudiante == form_data.username,
        )
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        _record_failed_attempt(rate_key)
        _log(db, "login_failed", ip=ip, detalle=f"intento fallido: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cuenta desactivada")

    token = create_access_token(subject=user.id, rol=user.rol)
    _log(db, "login_success", usuario_id=user.id, ip=ip)

    return TokenResponse(access_token=token, user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    """Retorna el perfil del usuario autenticado."""
    return current_user
