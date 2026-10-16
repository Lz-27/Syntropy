from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.schemas.user import UserOut
from app.schemas.file import ArchivoOut


class CategoriaOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    nombre: str
    descripcion: Optional[str] = None
    semana_numero: Optional[int] = None


class PostCreate(BaseModel):
    titulo: str
    resumen: Optional[str] = None
    contenido_markdown: str
    categoria_id: Optional[int] = None


class PostUpdate(BaseModel):
    titulo: Optional[str] = None
    resumen: Optional[str] = None
    contenido_markdown: Optional[str] = None
    categoria_id: Optional[int] = None
    is_pinned: Optional[bool] = None


class PostOut(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    titulo: str
    resumen: Optional[str] = None
    contenido_markdown: str
    autor_id: int
    categoria_id: Optional[int] = None
    vistas: int
    is_pinned: bool
    created_at: datetime
    updated_at: datetime
    autor: Optional[UserOut] = None
    categoria: Optional[CategoriaOut] = None
    archivos: List[ArchivoOut] = []


class PostListItem(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    titulo: str
    resumen: Optional[str] = None
    autor_id: int
    categoria_id: Optional[int] = None
    vistas: int
    is_pinned: bool
    created_at: datetime
    autor: Optional[UserOut] = None
    categoria: Optional[CategoriaOut] = None
    # Contadores (calculados en el servicio)
    total_archivos: int = 0
    total_comentarios: int = 0


class PaginatedPosts(BaseModel):
    total: int
    page: int
    limit: int
    items: List[PostListItem]
