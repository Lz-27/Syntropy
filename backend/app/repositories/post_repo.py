from typing import Optional, List, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, or_, desc, asc

from app.models.post import Post, Categoria
from app.models.file import Archivo
from app.models.comment import Comentario
from app.schemas.post import PostCreate, PostUpdate


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, post_id: int) -> Optional[Post]:
        return (
            self.db.query(Post)
            .options(
                joinedload(Post.autor),
                joinedload(Post.categoria),
                joinedload(Post.archivos),
            )
            .filter(Post.id == post_id)
            .first()
        )

    def increment_views(self, post_id: int) -> None:
        self.db.query(Post).filter(Post.id == post_id).update(
            {Post.vistas: Post.vistas + 1}, synchronize_session=False
        )
        self.db.commit()

    def list_posts(
        self,
        page: int = 1,
        limit: int = 10,
        categoria_id: Optional[int] = None,
        search: Optional[str] = None,
        order_by: str = "recent",
    ) -> Tuple[int, List[dict]]:
        query = self.db.query(Post).options(
            joinedload(Post.autor),
            joinedload(Post.categoria),
        )

        if categoria_id is not None:
            query = query.filter(Post.categoria_id == categoria_id)

        if search and search.strip():
            term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Post.titulo.ilike(term),
                    Post.resumen.ilike(term),
                    Post.contenido_markdown.ilike(term),
                )
            )

        total = query.count()

        # Ordenamiento
        if order_by == "views":
            query = query.order_by(Post.is_pinned.desc(), Post.vistas.desc(), Post.created_at.desc())
        elif order_by == "oldest":
            query = query.order_by(Post.is_pinned.desc(), Post.created_at.asc())
        else: # recent (default)
            query = query.order_by(Post.is_pinned.desc(), Post.created_at.desc())

        offset = (page - 1) * limit
        posts = query.offset(offset).limit(limit).all()

        # Calcular totales de archivos y comentarios para los posts obtenidos
        post_ids = [p.id for p in posts]
        archivos_counts = dict(
            self.db.query(Archivo.post_id, func.count(Archivo.id))
            .filter(Archivo.post_id.in_(post_ids))
            .group_by(Archivo.post_id)
            .all()
        ) if post_ids else {}

        comentarios_counts = dict(
            self.db.query(Comentario.post_id, func.count(Comentario.id))
            .filter(Comentario.post_id.in_(post_ids), Comentario.is_deleted == False)
            .group_by(Comentario.post_id)
            .all()
        ) if post_ids else {}

        items = []
        for p in posts:
            item_dict = {
                "id": p.id,
                "titulo": p.titulo,
                "resumen": p.resumen,
                "autor_id": p.autor_id,
                "categoria_id": p.categoria_id,
                "vistas": p.vistas,
                "is_pinned": p.is_pinned,
                "created_at": p.created_at,
                "autor": p.autor,
                "categoria": p.categoria,
                "total_archivos": archivos_counts.get(p.id, 0),
                "total_comentarios": comentarios_counts.get(p.id, 0),
            }
            items.append(item_dict)

        return total, items

    def create(self, post_data: PostCreate, autor_id: int) -> Post:
        post = Post(
            titulo=post_data.titulo,
            resumen=post_data.resumen,
            contenido_markdown=post_data.contenido_markdown,
            categoria_id=post_data.categoria_id,
            autor_id=autor_id,
        )
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update(self, post: Post, update_data: PostUpdate) -> Post:
        data = update_data.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(post, key, value)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()

    def get_stats(self, post_id: int) -> Optional[dict]:
        post = self.db.query(Post).filter(Post.id == post_id).first()
        if not post:
            return None
        total_archivos = self.db.query(func.count(Archivo.id)).filter(Archivo.post_id == post_id).scalar() or 0
        total_comentarios = self.db.query(func.count(Comentario.id)).filter(
            Comentario.post_id == post_id, Comentario.is_deleted == False
        ).scalar() or 0
        
        return {
            "post_id": post.id,
            "vistas": post.vistas,
            "total_archivos": total_archivos,
            "total_comentarios": total_comentarios,
            "total_reacciones": 0, # Se integra en P4
        }

    # Categorías
    def list_categories(self) -> List[Categoria]:
        return self.db.query(Categoria).order_by(Categoria.semana_numero.asc().nullslast(), Categoria.id.asc()).all()

    def get_category_by_id(self, categoria_id: int) -> Optional[Categoria]:
        return self.db.query(Categoria).filter(Categoria.id == categoria_id).first()
