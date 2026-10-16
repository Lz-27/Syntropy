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
