from datetime import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from app.schemas.user import UserOut


class ReaccionCreate(BaseModel):
    tipo: str = Field(..., pattern="^(aporte_valioso|duda|excelente_analisis)$")


class ReaccionOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    comentario_id: int
    usuario_id: int
    tipo: str
    created_at: datetime


class ComentarioCreate(BaseModel):
    contenido: str = Field(..., min_length=1, max_length=1500)
    padre_id: Optional[int] = None


class ComentarioUpdate(BaseModel):
    contenido: str = Field(..., min_length=1, max_length=1500)


class ComentarioOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    post_id: int
    usuario_id: int
    padre_id: Optional[int] = None
    contenido: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    usuario: Optional[UserOut] = None
    respuestas: List["ComentarioOut"] = []
    
    # Conteo de reacciones por tipo y reacción del usuario actual
    reacciones_conteo: Dict[str, int] = {
        "aporte_valioso": 0,
        "duda": 0,
        "excelente_analisis": 0,
    }
    user_reaction: Optional[str] = None


ComentarioOut.model_rebuild()
