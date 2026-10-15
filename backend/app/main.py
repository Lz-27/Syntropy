from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.core.database import create_tables
from app.routers import auth, posts, files

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


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "version": "1.0.0"}
