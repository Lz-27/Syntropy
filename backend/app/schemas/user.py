from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    nombre_completo: str
    codigo_estudiante: str
    email: EmailStr
    password: str

    @field_validator("codigo_estudiante")
    @classmethod
    def codigo_no_vacio(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("El código de estudiante no puede estar vacío")
        return v

    @field_validator("password")
    @classmethod
    def password_minlen(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v


class UserLogin(BaseModel):
    username: str   # email o código_estudiante
    password: str


class UserOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    codigo_estudiante: str
    nombre_completo: str
    email: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    rol: str
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
