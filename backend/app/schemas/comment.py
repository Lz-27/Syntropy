from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.schemas.user import UserOut


class ComentarioCreate(BaseModel):
    contenido: str
    padre_id: Optional[int] = None


class ComentarioUpdate(BaseModel):
    contenido: str


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


ComentarioOut.model_rebuild()
