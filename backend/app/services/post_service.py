from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.post_repo import PostRepository
from app.schemas.post import PostCreate, PostUpdate, PostListItem
from app.models.post import Post, Categoria
from app.models.user import User


class PostService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PostRepository(db)

    def list_posts(
        self,
        page: int = 1,
        limit: int = 10,
        categoria_id: Optional[int] = None,
        search: Optional[str] = None,
        order_by: str = "recent",
    ) -> Tuple[int, List[dict]]:
        if page < 1:
            page = 1
        if limit < 1 or limit > 50:
            limit = 10
        return self.repo.list_posts(
            page=page,
            limit=limit,
            categoria_id=categoria_id,
            search=search,
            order_by=order_by,
        )

    def get_post_detail(self, post_id: int, track_view: bool = True) -> Post:
        post = self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Publicación no encontrada",
            )
        if track_view:
            self.repo.increment_views(post_id)
            self.db.refresh(post)
        return post

    def create_post(self, post_data: PostCreate, current_user: User) -> Post:
        if post_data.categoria_id is not None:
            cat = self.repo.get_category_by_id(post_data.categoria_id)
            if not cat:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La categoría especificada no existe",
                )
        return self.repo.create(post_data, autor_id=current_user.id)

    def update_post(self, post_id: int, update_data: PostUpdate, current_user: User) -> Post:
        post = self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Publicación no encontrada",
            )

        # Autorización: propio autor o admin
        if post.autor_id != current_user.id and current_user.rol != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para editar esta publicación",
            )

        # Solo admin puede fijar posts
        if update_data.is_pinned is not None and current_user.rol != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo los administradores pueden fijar publicaciones",
            )

        if update_data.categoria_id is not None:
            cat = self.repo.get_category_by_id(update_data.categoria_id)
            if not cat:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La categoría especificada no existe",
                )

        return self.repo.update(post, update_data)

    def delete_post(self, post_id: int, current_user: User) -> None:
        post = self.repo.get_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Publicación no encontrada",
            )

        if post.autor_id != current_user.id and current_user.rol != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para eliminar esta publicación",
            )

        self.repo.delete(post)

    def get_post_stats(self, post_id: int) -> dict:
        stats = self.repo.get_stats(post_id)
        if not stats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Publicación no encontrada",
            )
        return stats

    def list_categories(self) -> List[Categoria]:
        return self.repo.list_categories()
