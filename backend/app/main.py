from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.database import create_tables
from app.routers import auth, posts, files, comments, users

# Crear directorio de uploads si no existe
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Crear tablas en BD
create_tables()

# ── FastAPI app factory ───────────────────────────────────────
app = FastAPI(
    title="TGS-Hub API",
    description="Plataforma académica colaborativa · Teoría General de Sistemas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Archivos estáticos (uploads) ──────────────────────────────
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# ── Routers ───────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(files.router)
app.include_router(comments.router)
app.include_router(users.router)


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/stats", tags=["system"])
def global_stats(db=None):
    """Estadísticas globales del ecosistema TGS-Hub para los KPIs del Dashboard."""
    from app.core.database import SessionLocal
    from app.models.post import Post
    from app.models.file import Archivo
    from app.models.comment import Comentario
    from app.models.user import User as UserModel

    session = SessionLocal()
    try:
        total_posts = session.query(Post).count()
        total_archivos = session.query(Archivo).count()
        total_comentarios = session.query(Comentario).filter(Comentario.is_deleted == False).count()
        usuarios_activos = session.query(UserModel).filter(UserModel.is_active == True).count()
        return {
            "total_posts": total_posts,
            "total_archivos": total_archivos,
            "total_comentarios": total_comentarios,
            "usuarios_activos": usuarios_activos,
        }
    finally:
        session.close()


@app.get("/analytics", tags=["analytics"])
def global_analytics():
    """Analíticas profundas del ecosistema TGS para gráficos Recharts y diagrama de Flujo Sistémico."""
    from sqlalchemy import func
    from app.core.database import SessionLocal
    from app.models.post import Post, Categoria
    from app.models.file import Archivo
    from app.models.comment import Comentario, ReaccionComentario as Reaccion
    from app.models.user import User as UserModel

    session = SessionLocal()
    try:
        # 1. Actividad por semana / categoría
        categorias = session.query(Categoria).order_by(Categoria.semana_numero.asc()).all()
        activity_by_week = []
        for cat in categorias:
            num_posts = session.query(Post).filter(Post.categoria_id == cat.id).count()
            # Comentarios en posts de esta categoría
            post_ids = [p.id for p in session.query(Post.id).filter(Post.categoria_id == cat.id).all()]
            num_comentarios = (
                session.query(Comentario).filter(Comentario.post_id.in_(post_ids), Comentario.is_deleted == False).count()
                if post_ids
                else 0
            )
            activity_by_week.append({
                "semana": f"Sem {cat.semana_numero}" if cat.semana_numero else cat.nombre[:10],
                "semana_num": cat.semana_numero or 0,
                "nombre": cat.nombre,
                "posts": num_posts,
                "comentarios": num_comentarios,
                "total": num_posts + num_comentarios,
            })

        # 2. Distribución de tipos de archivo
        ext_query = (
            session.query(
                Archivo.extension,
                func.count(Archivo.id).label("count"),
                func.sum(Archivo.tamano_bytes).label("total_bytes")
            )
            .group_by(Archivo.extension)
            .all()
        )
        file_types = [
            {
                "extension": ext.lower(),
                "name": ext.upper(),
                "count": count,
                "total_bytes": total_bytes or 0,
            }
            for ext, count, total_bytes in ext_query
        ]

        # 3. Top Contribuidores
        users = session.query(UserModel).filter(UserModel.is_active == True).all()
        contributors = []
        for u in users:
            posts_count = session.query(Post).filter(Post.autor_id == u.id).count()
            comments_count = session.query(Comentario).filter(Comentario.usuario_id == u.id, Comentario.is_deleted == False).count()
            # Archivos en posts de este autor
            author_post_ids = [p.id for p in session.query(Post.id).filter(Post.autor_id == u.id).all()]
            files_count = session.query(Archivo).filter(Archivo.post_id.in_(author_post_ids)).count() if author_post_ids else 0
            # Reacciones recibidas
            reactions_received = (
                session.query(Reaccion)
                .join(Comentario, Reaccion.comentario_id == Comentario.id)
                .filter(Comentario.usuario_id == u.id)
                .count()
            )

            score = (posts_count * 10) + (comments_count * 3) + (files_count * 5) + (reactions_received * 2)
            if score > 0:
                contributors.append({
                    "id": u.id,
                    "nombre_completo": u.nombre_completo,
                    "codigo_estudiante": u.codigo_estudiante,
                    "rol": u.rol,
                    "avatar_url": u.avatar_url,
                    "posts_count": posts_count,
                    "comments_count": comments_count,
                    "files_count": files_count,
                    "reactions_count": reactions_received,
                    "score": score,
                })

        contributors.sort(key=lambda x: x["score"], reverse=True)

        # 4. Flujo Sistémico TGS
        total_files = session.query(Archivo).count()
        total_posts = session.query(Post).count()
        total_views = session.query(func.sum(Post.vistas)).scalar() or 0
        total_comments = session.query(Comentario).filter(Comentario.is_deleted == False).count()
        total_reactions = session.query(Reaccion).count()

        tgs_flow = {
            "inputs": {
                "label": "Entradas (Inputs)",
                "sublabel": "Evidencias & Documentos",
                "value": total_files,
                "unit": "archivos",
            },
            "processes": {
                "label": "Procesamiento",
                "sublabel": "Artículos & Modelos TGS",
                "value": total_posts,
                "unit": "artículos",
            },
            "outputs": {
                "label": "Salidas (Outputs)",
                "sublabel": "Vistas & Transferencia",
                "value": total_views,
                "unit": "consultas",
            },
            "feedback": {
                "label": "Retroalimentación (Feedback)",
                "sublabel": "Debates & Reacciones",
                "value": total_comments + total_reactions,
                "unit": "interacciones",
            },
        }

        return {
            "activity_by_week": activity_by_week,
            "file_types": file_types,
            "top_contributors": contributors[:10],
            "tgs_flow": tgs_flow,
        }
    finally:
        session.close()
