from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    semana_numero: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_by_id: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="categoria", lazy="select")


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(300))
    resumen: Mapped[str | None] = mapped_column(Text, nullable=True)
    contenido_markdown: Mapped[str] = mapped_column(Text)
    autor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    categoria_id: Mapped[int | None] = mapped_column(ForeignKey("categorias.id"), nullable=True, index=True)
    vistas: Mapped[int] = mapped_column(Integer, default=0)
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    autor: Mapped["User"] = relationship(back_populates="posts")
    categoria: Mapped["Categoria"] = relationship(back_populates="posts")
    archivos: Mapped[list["Archivo"]] = relationship(back_populates="post", cascade="all, delete-orphan", lazy="select")
    comentarios: Mapped[list["Comentario"]] = relationship(back_populates="post", cascade="all, delete-orphan", lazy="select")
