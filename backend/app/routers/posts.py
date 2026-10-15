from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.audit import AuditoriaLog
from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostOut,
    PaginatedPosts,
    CategoriaOut,
)
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


def _log(db: Session, accion: str, usuario_id=None, entidad_id=None, ip=None, detalle=None):
    db.add(
        AuditoriaLog(
            accion=accion,
            usuario_id=usuario_id,
            entidad="post",
            entidad_id=entidad_id,
            ip=ip,
            detalle=detalle,
        )
    )
    db.commit()


@router.get("", response_model=PaginatedPosts)
def list_posts(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    categoria_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    order_by: str = Query("recent", pattern="^(recent|views|oldest)$"),
    db: Session = Depends(get_db),
):
    """Lista publicaciones con paginación, filtros de categoría y búsqueda."""
    service = PostService(db)
    total, items = service.list_posts(
        page=page,
        limit=limit,
        categoria_id=categoria_id,
        search=search,
        order_by=order_by,
    )
    return PaginatedPosts(
        total=total,
        page=page,
        limit=limit,
        items=items,
    )


@router.get("/categories", response_model=List[CategoriaOut])
def list_categories(db: Session = Depends(get_db)):
    """Lista todas las categorías académicas (semanas de TGS)."""
    service = PostService(db)
    return service.list_categories()


@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    body: PostCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Crea una nueva publicación (requiere autenticación)."""
    service = PostService(db)
    post = service.create_post(body, current_user)
    ip = request.client.host if request.client else None
    _log(db, "create_post", usuario_id=current_user.id, entidad_id=post.id, ip=ip, detalle=post.titulo)
    return post


@router.get("/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Obtiene el detalle de una publicación e incrementa sus vistas de forma atómica."""
    service = PostService(db)
    return service.get_post_detail(post_id, track_view=True)


@router.put("/{post_id}", response_model=PostOut)
def update_post(
    post_id: int,
    body: PostUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Edita una publicación existente (solo el autor o admin)."""
    service = PostService(db)
    post = service.update_post(post_id, body, current_user)
    ip = request.client.host if request.client else None
    _log(db, "update_post", usuario_id=current_user.id, entidad_id=post.id, ip=ip, detalle=post.titulo)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Elimina una publicación (solo el autor o admin)."""
    service = PostService(db)
    service.delete_post(post_id, current_user)
    ip = request.client.host if request.client else None
    _log(db, "delete_post", usuario_id=current_user.id, entidad_id=post_id, ip=ip)
    return None


@router.get("/{post_id}/stats")
def get_post_stats(post_id: int, db: Session = Depends(get_db)):
    """Retorna estadísticas de interacción de la publicación."""
    service = PostService(db)
    return service.get_post_stats(post_id)
